    public class SymbolTable{
        private Hashtable<String,String> DictionarySymbolTable; // taking to initialize dictionary
        private static final int START=16; //As the program start
        public SymbolTable() //making the constructor
        {
            this.DictionarySymbolTable = new Hashtable<String, String>();
            initializationDictionarySymbolTable();
        }
        //the dictionary init
        private void initializationDictionarySymbolTable() {
            this.DictionarySymbolTable.put("R0", "000000000000000");
            this.DictionarySymbolTable.put("R1", "000000000000001");
            this.DictionarySymbolTable.put("R2", "000000000000010");
            this.DictionarySymbolTable.put("R3", "000000000000011");
            this.DictionarySymbolTable.put("R4", "000000000000100");
            this.DictionarySymbolTable.put("R5", "000000000000101");
            this.DictionarySymbolTable.put("R6", "000000000000110");
            this.DictionarySymbolTable.put("R7", "000000000000111");
            this.DictionarySymbolTable.put("R8", "000000000001000");
            this.DictionarySymbolTable.put("R9", "000000000001001");
            this.DictionarySymbolTable.put("R10", "000000000001010");
            this.DictionarySymbolTable.put("R11", "000000000001011");
            this.DictionarySymbolTable.put("R12", "000000000001100");
            this.DictionarySymbolTable.put("R13", "000000000001101");
            this.DictionarySymbolTable.put("R14", "000000000001110");
            this.DictionarySymbolTable.put("R15", "000000000001111");
            this.DictionarySymbolTable.put("SP", "000000000000000");
            this.DictionarySymbolTable.put("LCL", "000000000000001");
            this.DictionarySymbolTable.put("ARG", "000000000000010");
            this.DictionarySymbolTable.put("THIS", "000000000000011");
            this.DictionarySymbolTable.put("THAT", "000000000000100");
            this.DictionarySymbolTable.put("SCREEN", "100000000000000");
            this.DictionarySymbolTable.put("KBD", "110000000000000");
        }
        public void addEntry (String symbol ,String address)
        {
            this.DictionarySymbolTable.put(symbol,address);
        }
        // check if there is symbol in this Dictionary
        public boolean contains(String symbol)
        {
            return this.DictionarySymbolTable.containsKey(symbol);
        }
        // return the address
        public String getAddress(String symbol)
        {
            return this.DictionarySymbolTable.get(symbol);
        }
        // to string function
        public String toString()
        {
            return this.DictionarySymbolTable.toString();
        }
    }
}
