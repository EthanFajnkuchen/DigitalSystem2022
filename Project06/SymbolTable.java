    import java.util.Hashtable;

public class SymbolTable{
    private Hashtable<String,Integer> DictionarySymbolTable; // taking to initialize dictionary
    private int RegiserNum; //As the program start
    public SymbolTable() //making the constructor
    {
        this.RegiserNum=16;
        this.DictionarySymbolTable = new Hashtable<String, Integer>();
        initializationDictionarySymbolTable();
    }
    //the dictionary init
    private void initializationDictionarySymbolTable() {
        this.DictionarySymbolTable.put("R0", 0);
        this.DictionarySymbolTable.put("R1", 1);
        this.DictionarySymbolTable.put("R2", 2);
        this.DictionarySymbolTable.put("R3", 3);
        this.DictionarySymbolTable.put("R4", 4);
        this.DictionarySymbolTable.put("R5",5);
        this.DictionarySymbolTable.put("R6", 6);
        this.DictionarySymbolTable.put("R7", 7);
        this.DictionarySymbolTable.put("R8", 8);
        this.DictionarySymbolTable.put("R9",9);
        this.DictionarySymbolTable.put("R10", 10);
        this.DictionarySymbolTable.put("R11", 11);
        this.DictionarySymbolTable.put("R12",12);
        this.DictionarySymbolTable.put("R13",13);
        this.DictionarySymbolTable.put("R14",14);
        this.DictionarySymbolTable.put("R15", 15);
        this.DictionarySymbolTable.put("SP", 0);
        this.DictionarySymbolTable.put("LCL", 1);
        this.DictionarySymbolTable.put("ARG", 2);
        this.DictionarySymbolTable.put("THIS", 3);
        this.DictionarySymbolTable.put("THAT", 4);
        this.DictionarySymbolTable.put("SCREEN", 16384);
        this.DictionarySymbolTable.put("KBD", 24576);
    }
    public int getRegiserNum()
    {
        int get =this.RegiserNum;
        return get;
    }
    public void addEntry (String symbol ,int address)
    {
        if (!contains(symbol)) {
            this.DictionarySymbolTable.put(symbol, address);
            this.RegiserNum++;
        }
    }
    // check if there is symbol in this Dictionary
    public boolean contains(String symbol)
    {
        return this.DictionarySymbolTable.containsKey(symbol);
    }
    // return the address
    public int getAddress(String symbol)
    {
        return this.DictionarySymbolTable.get(symbol);
    }
    // to string function
    public String toString()
    {
        return this.DictionarySymbolTable.toString();
    }
}
