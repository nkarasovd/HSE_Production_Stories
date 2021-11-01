package main.java;

public class Main {
    public static void main(String[] args) {
        SpellChecker sc = new SpellChecker("data/corpus.txt");
        sc.build_dict();
        for (String s : sc.suggest("doog")) {
            System.out.println(s);
        }
    }
}
