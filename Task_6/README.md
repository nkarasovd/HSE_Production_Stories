# Spell Checker

## Задача

Реализовать простой SpellChecker.

## Usage

`pip install -r requirements.txt`

`cd src_python`

`python simple_spell_checker.py --word doog --num_suggestions 3`

`python complicated_spell_checker.py --word doog --num_suggestions 3`

## Results

ComplicatedSpellChecker показал следующие
результаты на тестовом [датасете](http://aspell.net/test/cur/batch0.tab):

`Acc@1 = 0.45 | Acc@3 = 0.61 | Acc@5 = 0.68`.