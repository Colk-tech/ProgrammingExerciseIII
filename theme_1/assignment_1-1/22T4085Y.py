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
#
# - Game: ゲームの根本的なロジックを管理する。
# - (Tkinter)View: ゲームの表示を管理するクラス
# - Controller: ゲームの状態と表示を管理するクラス。Game と View を受け取り、それらを統括する。
#
# Game は他のクラスに依存してはならない。
# View は Game に依存してはならない。
# Controller は Game と View に依存する。


if __name__ == "__main__":
    pass
