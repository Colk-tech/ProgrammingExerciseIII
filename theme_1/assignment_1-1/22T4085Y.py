# Assignment '1-1' of Programming Exercise III at Ibaraki University, 2024
# Created on Apr 24, 2024 by 伊藤 愛基 / ITO Manaki (22T4085Y)
#
# This program is published on the internet at the following URL:
# https://github.com/Colk-tech/ProgrammingExerciseIII
#
# NOTE: If you notice that this program or a program very similar to this one is submitted as an assignment,
# it is likely that THE PERSON IN QUESTION has infringed the academic integrity policy.
# THIS PROGRAM IS THE ORIGINAL. DO NOT HAND IN THIS PROGRAM DESPITE IT IS PUBLIC.
# 注意: もしもこのプログラム、あるいは非常に類似のプログラムが課題として提出されているのを発見した場合、
# その者が学術倫理方針に違反している可能性があります。
# このプログラムがオリジナルです。このプログラムは公開されていますが、提出用に使用しないでください。
#
# # 設計方針
# 本来はそれぞれのクラスごとにファイルを分けたいが、1 ファイルで完結させるよう要求されているので、
# トップレベルのクラスを定義し、それぞれのクラスをネストすることで、1 ファイルで完結させる。
#
# また、このプログラムは MVC パターンに類似の設計を採用している。
# クラスの構成は以下の通りである。
# - ( Models: ゲームに用いるデータ構造を定義するクラス。 )
# - View: ゲームの表示を定義するクラス。
# - Controller: ゲームの制御を行うクラス。
#
# Game は他のクラスに依存してはならない。
# View は Game に依存してはならない。
# Controller は Game と View に依存する。
#
# このとうな設計にすることで、各クラスの責務を明確にし、それぞれのクラスを独立してテストできるようにする。

import tkinter as tk
from dataclasses import dataclass, field
from typing import Callable, Any, Literal, Optional


# dataclass はデータクラスを定義するためのデコレータである。
# データクラスは、データを保持するためのクラスであり、データの保持と操作を行うためのメソッドを持たない。
# ただし、バリデーションは行う。
@dataclass(frozen=True)
class Solution:
    text: str = field(default_factory=str)
    is_correct: bool = field(default=False)

    # バリデーションを行うメソッドを定義する。
    def validate_all(self):
        if not self.text:
            raise ValueError("Answer must not be empty.")

    # __post_init__ は dataclass によって提供される特殊なメソッドである。
    # このメソッドは、インスタンスが生成された後に自動で呼び出される。
    def __post_init__(self):
        self.validate_all()


@dataclass(frozen=True)
class Question:
    text: str = field(default_factory=str)
    solutions: list[Solution] = field(default_factory=list)
    score: int = field(default=0)

    def validate_all(self):
        if not self.text:
            raise ValueError("Question must not be empty.")

        if not self.solutions:
            raise ValueError("Answers must not be empty.")

        if not self.score >= 0:
            raise ValueError("Score must be greater than or equal to 0.")

    def __post_init__(self):
        self.validate_all()


@property
class EventData:
    event_type: Literal["start_clicked", "answer"] = field()
    selected_solution: Optional[Solution] = field(default=None)

    def validate_all(self):
        if not self.event_type:
            raise ValueError("Event type must not be empty.")

        if self.event_type == "answer" and not self.selected_solution:
            raise ValueError("Selected solution must not be empty.")

    def __post_init__(self):
        self.validate_all()


class EventBroker:
    def __init__(self):
        self.__listeners: list[Callable[[EventData], Any]] = []

    def add_listener(self, listener: Callable[[EventData], Any]):
        self.__listeners.append(listener)

    def notify(self, event_data: EventData):
        for listener in self.__listeners:
            listener(event_data)


# ゲームの表示を定義する。
# ゲームの表示は、ウィンドウの表示、ボタンの表示、ラベルの表示などを行う。
class View:
    WINDOW_SIZE_XY = (550, 350)
    WINDOW_SIZE_XY_STR = f"{WINDOW_SIZE_XY[0]}x{WINDOW_SIZE_XY[1]}"

    WINDOW_CENTER_X = WINDOW_SIZE_XY[0] // 2
    WINDOW_CENTER_Y = WINDOW_SIZE_XY[1] // 2

    WINDOW_TITLE = "Quiz Game"

    class Frames:
        class FrameBase:
            def __init__(self):
                self.__frame = tk.Frame()
                self.__frame.grid(row=0, column=0, sticky="nsew")

                self.__frame.grid_rowconfigure(0, weight=1)
                self.__frame.grid_rowconfigure(1, weight=1)
                self.__frame.grid_columnconfigure(0, weight=1)

            @property
            def frame(self):
                return self.__frame

        class TitleFrame(FrameBase):
            def __init__(self):
                super().__init__()

                self.__setup_design()

            def __setup_design(self):
                self.__title_label = tk.Label(
                    self.frame,
                    text="Quiz Game",
                    font=(None, '64')
                )
                self.__title_label.grid(row=0, column=0, padx=10, pady=10)

                self.__start_button = tk.Button(
                    self.frame,
                    text="Start",
                    width=10,
                    height=2,
                )
                self.__start_button.grid(row=1, column=0, padx=10, pady=10)

        class QuestionFrame(FrameBase):
            def __init__(self, question: Question):
                super().__init__()

                self.__question: Question = question

                self.__setup_design()

            def __setup_design(self):
                self.__question_label = tk.Label(
                    self.frame,
                    text=self.__question.text,
                    font=(None, '32')
                )
                self.__question_label.grid(
                    row=0,
                    column=0,
                    pady=10,
                )

                self.__answer_buttons: list[tk.Button] = []
                for i, solution in enumerate(self.__question.solutions):
                    button = tk.Button(
                        self.frame,
                        text=i,
                        width=10,
                        height=2,
                    )

                    solution_text_label = tk.Label(
                        self.frame,
                        text=solution.text,
                        font=(None, '24')
                    )

                    button.grid(row=i + 1, column=0, padx=100, pady=10)
                    solution_text_label.grid(row=i + 1, column=1, padx=10, pady=10)

                    self.__answer_buttons.append(button)

    def __init__(self):
        self.__root: tk.Tk = tk.Tk()

        self.__root.title(self.WINDOW_TITLE)
        self.__root.geometry(self.WINDOW_SIZE_XY_STR)

        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)

    def run(self):
        self.__root.tkraise(self.Frames.TitleFrame().frame)

        self.__root.mainloop()


class Controller:
    SAMPLE_QUESTIONS: list[Question] = [
        Question(
            text="What is 1 + 1?",
            solutions=[
                Solution(text="1", is_correct=False),
                Solution(text="2", is_correct=True),
                Solution(text="3", is_correct=False),
                Solution(text="4", is_correct=False),
            ],
            score=100
        ),
        Question(
            text="Which is the correct answer for ∫x dx?",
            solutions=[
                Solution(text="1/2 x^2 + C", is_correct=True),
                Solution(text="x^2 + C", is_correct=False),
                Solution(text="x + C", is_correct=False),
                Solution(text="1 + C", is_correct=False),
            ],
            score=100
        ),
        Question(
            text="What is the capital of France?",
            solutions=[
                Solution(text="Paris", is_correct=True),
                Solution(text="Lyon", is_correct=False),
                Solution(text="Marseille", is_correct=False),
                Solution(text="Nice", is_correct=False),
            ],
            score=100
        ),
        Question(
            text="Which of the following is a prime number?",
            solutions=[
                Solution(text="13", is_correct=True),
                Solution(text="21", is_correct=False),
                Solution(text="57", is_correct=False),
                Solution(text="169", is_correct=False),
            ],
            score=100
        ),
    ]


if __name__ == "__main__":
    View().run()
