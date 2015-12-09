## Trie Again - 80 (Algo) ##

#### Write-up by patil215

Created: 2015-12-08

### Problem ###

How many words can you find in the given table with the given dictionary?

### Files ###
[words.txt](https://compete.sctf.io/2015q2/problemfiles/40/words.txt)

[lettergrid.png](https://compete.sctf.io/2015q2/problemfiles/40/lettergrid.png)

### Hint ###

Words are found by going up, down, left, right, or diagonally. A letter can only be used once per word.


## Answer ##

### Overview ###

Create a list of words from the file that can be made by the grid. Then generate all permutations of words that can be made off of the grid. Lastly, compare the permutations to the possible words efficiently using a trie data structure, or inefficiently (but more easily) with a set.

### Details ###

Looking at the problem, it's clear that we need to first generate a list of all the possible permutations of words that can be made. However, before we start on that, there is one thing we can do to make our lives a bit easier.

The file ```words.txt``` has 235887 lines. Wouldn't it be nice if we could cut that down a bit? One simple way to do that is to filter out the words that can't be made by the letters in the grid - since the letters in the grid only contain 12 of the 26 letters in the alphabet.

Some Java code to do this:
```java
final Scanner scan = new Scanner(new File("words.txt"));
final PrintWriter writer = new PrintWriter(new File("condensedwords.txt"));
final char[] gridChars = new char[] {'e', 'c', 'a', 'l', 'p', 'h', 'n', 'b', 'o', 'q', 't', 'y'};
while(scan.hasNextLine()) {
    final String word = scan.nextLine().toLowerCase();

    boolean allValidChars = true;
    for(int i = 0; i < word.length(); i++) {
        boolean validChar = false;
        for(int d = 0; d < gridChars.length; d++) {
            if(word.charAt(i) == gridChars[d]) {
                validChar = true;
            }
        }
        if(!validChar) {
            allValidChars = false;
        }
    }
    if(allValidChars) {
        writer.println(word);
    }
}
writer.close();
```

Looking now at ```condensedwords.txt```, we now have a much more manageable 3729 words. Notably, this is a small enough list where we could actually iterate through all of them to check instead of using the more efficient trie - an explanation of this soon.

Now, we need a way of generating all possible words that can be made on the grid. The hint says words are found going up, down, left, or diagonally, and only one grid letter can be used per word. One way to generate all possible words, then, would be to write a recursive solution that takes in a list of words that can be made, the grid, a current position (x and y), the current word string, and a boolean grid of letters that have been used.

Then, we can iterate through all of these paths, and check them with the list of words we have. Since the list is small (~3000 words), we can just do a double for loop. A more efficient solution is to use a trie (more on that later).

Here is the code. Disclaimer: this is by no means the most concise, readable, or efficient way of doing this.

```java
private static ArrayList<String> returnPaths(ArrayList<String> cur, char[][] grid, int x, int y, String startingString, boolean[][] lettersUsed) {
    startingString += grid[x][y];
    lettersUsed[x][y] = true;
    cur.add(startingString);

    // Check right
    if(x < grid.length - 1 && !lettersUsed[x + 1][y]) {
        boolean[][] newLettersUsed = new boolean[4][4];
        for(int i = 0; i < 4; i++) {
            for(int d = 0; d < 4; d++) {
                newLettersUsed[i][d] = lettersUsed[i][d];
            }
        }
        returnPaths(cur, grid, x+1, y, startingString, newLettersUsed);
    }

    // Check left
    if(x > 0 && !lettersUsed[x - 1][y]) {
        boolean[][] newLettersUsed = new boolean[4][4];
        for(int i = 0; i < 4; i++) {
            for(int d = 0; d < 4; d++) {
                newLettersUsed[i][d] = lettersUsed[i][d];
            }
        }
        returnPaths(cur, grid, x - 1, y, startingString, newLettersUsed);
    }

    // Check down
    if(y < grid[0].length - 1 && !lettersUsed[x][y + 1]) {
        boolean[][] newLettersUsed = new boolean[4][4];
        for(int i = 0; i < 4; i++) {
            for(int d = 0; d < 4; d++) {
                newLettersUsed[i][d] = lettersUsed[i][d];
            }
        }
        returnPaths(cur, grid, x, y + 1, startingString, newLettersUsed);
    }


    // Check up
    if(y > 0 && !lettersUsed[x][y - 1]) {
        boolean[][] newLettersUsed = new boolean[4][4];
        for(int i = 0; i < 4; i++) {
            for(int d = 0; d < 4; d++) {
                newLettersUsed[i][d] = lettersUsed[i][d];
            }
        }
        returnPaths(cur, grid, x, y - 1, startingString, newLettersUsed);
    }

    // Check bottom right
    if(x < grid.length - 1 && y < grid[0].length - 1 && !lettersUsed[x + 1][y + 1]) {
        boolean[][] newLettersUsed = new boolean[4][4];
        for(int i = 0; i < 4; i++) {
            for(int d = 0; d < 4; d++) {
                newLettersUsed[i][d] = lettersUsed[i][d];
            }
        }
        returnPaths(cur, grid, x + 1, y + 1, startingString, newLettersUsed);

    }

    // Check bottom left
    if(x > 0 && y < grid[0].length - 1 && !lettersUsed[x - 1][y + 1]) {
        boolean[][] newLettersUsed = new boolean[4][4];
        for(int i = 0; i < 4; i++) {
            for(int d = 0; d < 4; d++) {
                newLettersUsed[i][d] = lettersUsed[i][d];
            }
        }
        returnPaths(cur, grid, x - 1, y + 1, startingString, newLettersUsed);

    }

    // Check top right
    if(x < grid.length - 1 && y > 0 && !lettersUsed[x + 1][y - 1]) {
        boolean[][] newLettersUsed = new boolean[4][4];
        for(int i = 0; i < 4; i++) {
            for(int d = 0; d < 4; d++) {
                newLettersUsed[i][d] = lettersUsed[i][d];
            }
        }
        returnPaths(cur, grid, x + 1, y - 1, startingString, lettersUsed);

    }

    // Check top left
    if(x > 0 && y > 0 && !lettersUsed[x - 1][y - 1]) {
        boolean[][] newLettersUsed = new boolean[4][4];
        for(int i = 0; i < 4; i++) {
            for(int d = 0; d < 4; d++) {
                newLettersUsed[i][d] = lettersUsed[i][d];
            }
        }
        returnPaths(cur, grid, x - 1, y - 1, startingString, lettersUsed);
    }
    return cur;
}

public static void main(String[] args) throws FileNotFoundException {
    final Scanner scan = new Scanner(new File("words.txt"));
    final PrintWriter writer = new PrintWriter(new File("condensedwords.txt"));
    final char[] gridChars = new char[] {'e', 'c', 'a', 'l', 'p', 'h', 'n', 'b', 'o', 'q', 't', 'y'};
    while(scan.hasNextLine()) {
        final String word = scan.nextLine().toLowerCase();

        boolean allValidChars = true;
        for(int i = 0; i < word.length(); i++) {
            boolean validChar = false;
            for(int d = 0; d < gridChars.length; d++) {
                if(word.charAt(i) == gridChars[d]) {
                    validChar = true;
                }
            }
            if(!validChar) {
                allValidChars = false;
            }
        }
        if(allValidChars) {
            writer.println(word);
        }
    }
    writer.close();

    Scanner scanner = new Scanner(new File("condensedwords.txt"));

    HashSet<String> words = new HashSet<String>();
    HashSet<String> matchingWords = new HashSet<String>();

    while(scanner.hasNextLine()) {
        String word = scanner.nextLine().toLowerCase();
        words.add(word);
    }
    System.out.println(words.size());

    // Compare the words to the paths
    char[][] grid = new char[][] {{'e', 'e', 'c', 'a'}, {'a', 'l', 'e', 'p'}, {'h', 'n', 'b', 'o'}, {'q', 't', 't', 'y'}};

    // Iterate through starting characters on grid
    for(int i = 0; i < 4; i++) {
        for(int d = 0; d < 4; d++) {
            boolean[][] lettersUsed = new boolean[grid.length][grid[0].length];
            ArrayList<String> paths = returnPaths(new ArrayList<String>(), grid, i, d, "", lettersUsed);
            for(int r = 0; r < paths.size(); r++) {
                if(words.contains(paths.get(r))) {
                    matchingWords.add(paths.get(r));
                }
            }
        }
    }

    System.out.println(matchingWords.size()); // The flag
}
```

Now, it seems like this solution violates the spirit of the problem. The name implies we're supposed to use a trie! For those of y'all that don't know what a trie is, [this source](http://www.toptal.com/java/the-trie-a-neglected-data-structure) has a decent explanation that also happens to be related to the problem. Using a trie, one could solve the problem by adding all words to the structure, then, for each possible path on the grid, checking if that path exists within the trie.

Here's the entire class for how that could be implemented. For the trie, I used a simple implementation online.

```java
import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.*;

/**
* Implements very fast dictionary storage and retrieval.
* Only depends upon the core String class.
*
* // Credit:
* @author Melinda Green - © 2010 Superliminal Software.
* Free for all uses with attribution.
*/
public class TrieMap {

    private Object[] mChars = new Object[256];
    private Object mPrefixVal; // Used only for values of prefix keys.
    
    // Simple container for a string-value pair.
    private static class Leaf {
        public String mStr;
        public Object mVal;
        public Leaf(String str, Object val) {
            mStr = str;
            mVal = val;
        }
    }
    
    public TrieMap() {
    }
    
    public boolean isEmpty() {
        if(mPrefixVal != null) {
            return false;
        }
        for(Object o : mChars) {
            if(o != null) {
                return false;
            }
        }
        return true;
    }
    
    
    /**
     * Inserts a key/value pair.
     *
     * @param key may be empty or contain low-order chars 0..255 but must not be null.
     * @param val Your data. Any data class except another TrieMap. Null values erase entries.
     */
    public void put(String key, Object val) {
        assert key != null;
        assert !(val instanceof TrieMap); // Only we get to store TrieMap nodes. TODO: Allow it.
        if(key.length() == 0) {
            // All of the original key's chars have been nibbled away 
            // which means this node will store this key as a prefix of other keys.
            mPrefixVal = val; // Note: possibly removes or updates an item.
            return;
        }
        char c = key.charAt(0);
        Object cObj = mChars[c];
        if(cObj == null) { // Unused slot means no collision so just store and return;
            if(val == null) {
                return; // Don't create a leaf to store a null value.
            }
            mChars[c] = new Leaf(key, val);
            return;
        }
        if(cObj instanceof TrieMap) {
            // Collided with an existing sub-branch so nibble a char and recurse.
            TrieMap childTrie = (TrieMap)cObj;
            childTrie.put(key.substring(1), val);
            if(val == null && childTrie.isEmpty()) {
                mChars[c] = null; // put() must have erased final entry so prune branch.
            }
            return;
        }
        // Collided with a leaf 
        if(val == null) {
            mChars[c] = null; // Null value means to remove any previously stored value.
            return;
        }
        assert cObj instanceof Leaf;
        // Sprout a new branch to hold the colliding items.
        Leaf cLeaf = (Leaf)cObj;
        TrieMap branch = new TrieMap();
        branch.put(key.substring(1), val); // Store new value in new subtree.
        branch.put(cLeaf.mStr.substring(1), cLeaf.mVal); // Plus the one we collided with.
        mChars[c] = branch;
    }
    
    
    /**
     * Retrieve a value for a given key or null if not found.
     */
    public Object get(String key) {
        assert key != null;
        if(key.length() == 0) {
            // All of the original key's chars have been nibbled away 
            // which means this key is a prefix of another.
            return mPrefixVal;
        }
        char c = key.charAt(0);
        Object cVal = mChars[c];
        if(cVal == null) {
            return null; // Not found.
        }
        assert cVal instanceof Leaf || cVal instanceof TrieMap;
        if(cVal instanceof TrieMap) { // Hash collision. Nibble first char, and recurse.
            return ((TrieMap)cVal).get(key.substring(1));
        }
        if(cVal instanceof Leaf) {
            // cVal contains a user datum, but does the key match its substring?
            Leaf cPair = (Leaf)cVal;
            if(key.equals(cPair.mStr)) {
                return cPair.mVal; // Return user's data value.
            }
        }
        return null; // Not found.
    }
    
    private static ArrayList<String> returnPaths(ArrayList<String> cur, char[][] grid, int x, int y, String startingString, boolean[][] lettersUsed) {
        startingString += grid[x][y];
        lettersUsed[x][y] = true;
        cur.add(startingString);
    
        // Check right
        if(x < grid.length - 1 && !lettersUsed[x + 1][y]) {
            boolean[][] newLettersUsed = new boolean[4][4];
            for(int i = 0; i < 4; i++) {
                for(int d = 0; d < 4; d++) {
                    newLettersUsed[i][d] = lettersUsed[i][d];
                }
            }
            returnPaths(cur, grid, x+1, y, startingString, newLettersUsed);
        }
    
        // Check left
        if(x > 0 && !lettersUsed[x - 1][y]) {
            boolean[][] newLettersUsed = new boolean[4][4];
            for(int i = 0; i < 4; i++) {
                for(int d = 0; d < 4; d++) {
                    newLettersUsed[i][d] = lettersUsed[i][d];
                }
            }
            returnPaths(cur, grid, x - 1, y, startingString, newLettersUsed);
        }
    
        // Check down
        if(y < grid[0].length - 1 && !lettersUsed[x][y + 1]) {
            boolean[][] newLettersUsed = new boolean[4][4];
            for(int i = 0; i < 4; i++) {
                for(int d = 0; d < 4; d++) {
                    newLettersUsed[i][d] = lettersUsed[i][d];
                }
            }
            returnPaths(cur, grid, x, y + 1, startingString, newLettersUsed);
        }
    
    
        // Check up
        if(y > 0 && !lettersUsed[x][y - 1]) {
            boolean[][] newLettersUsed = new boolean[4][4];
            for(int i = 0; i < 4; i++) {
                for(int d = 0; d < 4; d++) {
                    newLettersUsed[i][d] = lettersUsed[i][d];
                }
            }
            returnPaths(cur, grid, x, y - 1, startingString, newLettersUsed);
        }
    
        // Check bottom right
        if(x < grid.length - 1 && y < grid[0].length - 1 && !lettersUsed[x + 1][y + 1]) {
            boolean[][] newLettersUsed = new boolean[4][4];
            for(int i = 0; i < 4; i++) {
                for(int d = 0; d < 4; d++) {
                    newLettersUsed[i][d] = lettersUsed[i][d];
                }
            }
            returnPaths(cur, grid, x + 1, y + 1, startingString, newLettersUsed);
    
        }
    
        // Check bottom left
        if(x > 0 && y < grid[0].length - 1 && !lettersUsed[x - 1][y + 1]) {
            boolean[][] newLettersUsed = new boolean[4][4];
            for(int i = 0; i < 4; i++) {
                for(int d = 0; d < 4; d++) {
                    newLettersUsed[i][d] = lettersUsed[i][d];
                }
            }
            returnPaths(cur, grid, x - 1, y + 1, startingString, newLettersUsed);
    
        }
    
        // Check top right
        if(x < grid.length - 1 && y > 0 && !lettersUsed[x + 1][y - 1]) {
            boolean[][] newLettersUsed = new boolean[4][4];
            for(int i = 0; i < 4; i++) {
                for(int d = 0; d < 4; d++) {
                    newLettersUsed[i][d] = lettersUsed[i][d];
                }
            }
            returnPaths(cur, grid, x + 1, y - 1, startingString, lettersUsed);
    
        }
    
        // Check top left
        if(x > 0 && y > 0 && !lettersUsed[x - 1][y - 1]) {
            boolean[][] newLettersUsed = new boolean[4][4];
            for(int i = 0; i < 4; i++) {
                for(int d = 0; d < 4; d++) {
                    newLettersUsed[i][d] = lettersUsed[i][d];
                }
            }
            returnPaths(cur, grid, x - 1, y - 1, startingString, lettersUsed);
        }
        return cur;
    }
    
    public static void main(String[] args) throws FileNotFoundException {
        final Scanner scan = new Scanner(new File("words.txt"));
        final PrintWriter writer = new PrintWriter(new File("condensedwords.txt"));
        final char[] gridChars = new char[] {'e', 'c', 'a', 'l', 'p', 'h', 'n', 'b', 'o', 'q', 't', 'y'};
        while(scan.hasNextLine()) {
            final String word = scan.nextLine().toLowerCase();
    
            boolean allValidChars = true;
            for(int i = 0; i < word.length(); i++) {
                boolean validChar = false;
                for(int d = 0; d < gridChars.length; d++) {
                    if(word.charAt(i) == gridChars[d]) {
                        validChar = true;
                    }
                }
                if(!validChar) {
                    allValidChars = false;
                }
            }
            if(allValidChars) {
                writer.println(word);
            }
        }
        writer.close();
    
        Scanner scanner = new Scanner(new File("condensedwords.txt"));
    
        HashSet<String> matchingWords = new HashSet<String>();
    
        TrieMap trieMap = new TrieMap();
    
        while(scanner.hasNextLine()) {
            String word = scanner.nextLine().toLowerCase();
            trieMap.put(word, word);
        }
    
        // Compare the words to the paths
        char[][] grid = new char[][] {{'e', 'e', 'c', 'a'}, {'a', 'l', 'e', 'p'}, {'h', 'n', 'b', 'o'}, {'q', 't', 't', 'y'}};
    
        // Iterate through starting characters on grid
        for(int i = 0; i < 4; i++) {
            for(int d = 0; d < 4; d++) {
                boolean[][] lettersUsed = new boolean[grid.length][grid[0].length];
                ArrayList<String> paths = returnPaths(new ArrayList<String>(), grid, i, d, "", lettersUsed);
                for(int r = 0; r < paths.size(); r++) {
                    if(trieMap.get(paths.get(r)) != null) {
                        matchingWords.add(paths.get(r));
                    }
                }
            }
        }
    
        System.out.println(matchingWords.size()); // The flag
    }
}
```

Both methods (using the HashSet and the Trie) return 156. However, I found this solution has an off by one error - it's actually the output of the program plus one. I believe this is because the ```words.txt``` file has two newlines at the end - meaning one is a blank string which could technically be "made" by the grid by not moving on any letters. That gives a flag of 157, which is correct.


### Flag ###

	157