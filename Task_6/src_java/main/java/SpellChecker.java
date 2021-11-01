package main.java;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;

public class SpellChecker {

    private final String dict_path;
    Map<String, Integer> counterMap = new HashMap<>();

    public SpellChecker(String dict_path) {
        this.dict_path = dict_path;
    }

    public void build_dict() {
        Scanner sc2 = null;
        try {
            sc2 = new Scanner(new File(this.dict_path));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }


        while (sc2.hasNextLine()) {
            Scanner s2 = new Scanner(sc2.nextLine());
            while (s2.hasNext()) {
                String s = s2.next().toLowerCase();
                this.counterMap.compute(s, (k, v) -> v == null ? 1 : v + 1);
            }
        }
    }

    public Set<String> get_1_edit(String word) {
        int n = word.length();
        String[] deletion = new String[n];

        for (int i = 0; i < n; i++) {
            deletion[i] = word.substring(0, i) + word.substring(i + 1);
        }

        String[] insertion = new String[26 * n];
        for (int i = 0; i < n; i++) {
            int w = 0;
            for (char c : "abcdefghijklmnopqrstuvwxyz".toCharArray()) {
                insertion[i * 26 + w] = word.substring(0, i) + c + word.substring(i);
                w += 1;
            }
        }

        String[] alteration = new String[26 * n];
        for (int i = 0; i < n; i++) {
            int w = 0;
            for (char c : "abcdefghijklmnopqrstuvwxyz".toCharArray()) {
                alteration[i * 26 + w] = word.substring(0, i) + c + word.substring(i + 1);
                w += 1;
            }
        }

        String[] transposition = new String[n - 1];
        for (int i = 0; i < n - 1; i++) {
            transposition[i] = word.substring(0, i) + word.charAt(i + 1) + word.charAt(i) + word.substring(i + 2);
        }

        Set<String> targetSet = new HashSet<String>();
        Collections.addAll(targetSet, deletion);
        Collections.addAll(targetSet, insertion);
        Collections.addAll(targetSet, alteration);
        Collections.addAll(targetSet, transposition);
        return targetSet;
    }

    public Set<String> get_known_words_edit_2_symbol(String word) {
        Set<String> targetSet = new HashSet<String>();
        Set<String> edit_1 = this.get_1_edit(word);
        for (String s : edit_1) {
            Set<String> edit_2 = this.get_1_edit(s);
            for (String s2 : edit_2) {
                if (counterMap.containsKey(s2)) {
                    targetSet.add(s2);
                }
            }
        }
        return targetSet;
    }

    public Set<String> known(Set<String> words) {
        Set<String> result = new HashSet<String>();
        for (String word : words) {
            if (this.counterMap.containsKey(word)) {
                result.add(word);
            }
        }
        return result;
    }

    public List<String> suggest(String word) {
        Set<String> result = new HashSet<String>();
        Set<String> r0 = new HashSet<String>();
        r0.add(word);
        Set<String> r1 = this.known(this.get_1_edit(word));
        Set<String> r2 = this.known(r0);
        Set<String> r3 = this.get_known_words_edit_2_symbol(word);

        if (r2.size() > 0) {
            result.addAll(r2);
        } else if (r1.size() > 0) {
            result.addAll(r1);
        } else if (r3.size() > 0) {
            result.addAll(r3);
        } else {
            result.addAll(r0);
        }

        List<String> sortedList = new ArrayList<>(result);
        sortedList.sort(Comparator.comparing(a -> -this.counterMap.get(a)));

        return sortedList;
    }

}
