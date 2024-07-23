<?php
declare(strict_types=1);

$filename = 'todos.txt';
if (!file_exists($filename)) touch($filename); // ファイルが無い時は作成

/**
 * タスクの形式について:
 *
 * 1行に1つのタスクを記述
 *
 * タスクの形式は「id \t task \t status」
 * タブ区切りで3つの要素を記述
 * id: タスクの一意なID (UNIXタイムスタンプ)
 * task: タスクの内容
 * status: タスクの状態 (incomplete: 未完了, complete: 完了)
 */

/**
 * ファイルからタスクを読み込む関数
 *
 * @param string $filename
 * @return array<int, array{id: int, task: string, status: string}>
 */
function readTasks(string $filename): array
{
    $tasks = [];
    if (!file_exists($filename) || !is_readable($filename)) {
        return $tasks; // ファイルが存在しないか、読み込み不可の場合は空の配列を返す
    }

    $lines = file($filename, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES); // 空行を無視するオプションを追加
    if ($lines === false) {
        return $tasks; // ファイル読み込みに失敗した場合は空の配列を返す
    }

    foreach ($lines as $line) {
        list($id, $task, $status) = explode("\t", $line);
        $tasks[] = ['id' => (int)$id, 'task' => $task, 'status' => $status]; // タブ区切りで分割して連想配列に格納
    }

    return $tasks;
}

/**
 * タスクをファイルに書き込む関数
 *
 * @param string $filename
 * @param array<int, array{id: int, task: string, status: string}> $tasks
 * @return void
 */
function writeTasks(string $filename, array $tasks): void
{
    $file = fopen($filename, 'w');
    if ($file === false) {
        die('ファイルを開けません');
    }

    if (!flock($file, LOCK_EX)) {
        fclose($file);
        die('ファイルのロックに失敗しました');
    }

    foreach ($tasks as $task) {

        fwrite($file, implode("\t", $task) . PHP_EOL); // task をタブ区切りで書き込む
    }

    flock($file, LOCK_UN);
    fclose($file);
}

$tasks = readTasks($filename);
$message = '';
if (!empty($_POST['task'])) { // タスク登録フォームが送信された場合
    $task = trim($_POST['task']);
    if ($task !== '') {
        $id = time();
        $status = 'incomplete';
        $tasks[] = ['id' => $id, 'task' => $task, 'status' => $status];
        writeTasks($filename, $tasks);
        // タスク登録メッセージ
        // htmlspecialchars() でエスケープ処理を行う (XSS対策)
        $message = htmlspecialchars("「{$task}」を登録しました", ENT_QUOTES, 'UTF-8');
    } else {
        $message = 'タスクの内容を入力してください';
    }
} elseif (isset($_POST['complete'])) { // 完了ボタンが押された場合
    $id = (int)$_POST['complete'];
    // タスクの status を complete に変更
    foreach ($tasks as &$task) {
        if ($task['id'] === $id) {
            $task['status'] = 'complete';
            break;
        }
    }
    // unset() で参照を削除
    // 参照を削除しないと、後続の処理で $task が参照している配列要素が変更されてしまう
    unset($task);
    writeTasks($filename, $tasks); // 編集後のタスクをファイルに書き込む
    $message = "タスクを完了しました";
} elseif (isset($_POST['delete'])) { // 削除ボタンが押された場合
    $id = (int)$_POST['delete'];
    // array_filter() で削除対象のタスクを除外して新しい配列を作成
    // array_filter() の第2引数に無名関数を渡して、削除対象のタスクを除外する
    // fn() は無名関数の省略記法
    $tasks = array_filter($tasks, fn($task) => $task['id'] !== $id);
    writeTasks($filename, $tasks); // 編集後のタスクをファイルに書き込む
    $message = "タスクを削除しました";
}

$tasks = readTasks($filename); // 更新されたタスクを再読み込み
?>

<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>TODOアプリ</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f8ff;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .container {
            background-color: #ffffff;
            padding: 2em;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 80%;
            max-width: 600px;
            text-align: center;
        }

        h1 {
            color: #007BFF;
            font-size: 24px;
            margin-bottom: 20px;
        }

        form {
            margin-bottom: 20px;
        }

        input[type="text"] {
            width: calc(100% - 22px);
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }

        input[type="submit"], button {
            background-color: #007BFF;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
        }

        input[type="submit"]:hover, button:hover {
            background-color: #0056b3;
        }

        ul {
            list-style-type: none;
            padding: 0;
        }

        li {
            background-color: #f8f9fa;
            margin: 5px 0;
            padding: 10px;
            border-radius: 4px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .task-complete {
            text-decoration: line-through;
            color: #6c757d;
        }

        .task-buttons {
            display: flex;
            gap: 5px;
        }

        .task-name {
            flex-grow: 1;
            text-align: right;
            margin-right: 10px;
        }

        .button-disabled {
            background-color: #c0c0c0;
            cursor: not-allowed;
        }

        .message {
            margin-bottom: 20px;
            color: #007BFF;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>TODOアプリ</h1>
    <?php if ($message): ?>
        <p class="message"><?= $message ?></p>
    <?php endif; ?>
    <form method="POST" action="kadai2-2.php">
        <label>
            登録したいタスクを入力...
            <input type="text" name="task" size="20" required/>
        </label>
        <input type="submit" value="登録"/><br/>
    </form>
    <h2>登録済みタスク</h2>
    <ul>
        <?php foreach ($tasks as $task): ?>
            <li>
                    <span class="task-name <?= $task['status'] === 'complete' ? 'task-complete' : '' ?>">
                        <!-- $task['status'] === 'complete' の場合はタスク名に [完了] を付ける (三項演算子) -->
                        <?= $task['status'] === 'complete' ? '[完了] ' : '' ?>
                        <?= htmlspecialchars($task['task'], ENT_QUOTES, 'UTF-8') ?> 
                    </span>
                <div class="task-buttons">
                    <form method="POST" action="kadai2-2.php" style="display:inline;">
                        <!-- 完了ボタンは完了済みのタスクには無効化する (三項演算子) -->
                        <button type="submit" name="complete"
                                value="<?= $task['id'] ?>"
                            <?= $task['status'] === 'complete' ? 'disabled class="button-disabled"' : '' ?>>
                            完了
                        </button>
                    </form>
                    <form method="POST" action="kadai2-2.php" style="display:inline;">
                        <button type="submit" name="delete" value="<?= $task['id'] ?>">削除</button>
                    </form>
                </div>
            </li>
        <?php endforeach; ?>
    </ul>
</div>
</body>
</html>
