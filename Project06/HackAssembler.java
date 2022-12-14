import java.nio.charset.StandardCharsets;
import java.util.*;
public class HackAssembler {
    public class Code {
        private Hashtable<String,String> destTable;
        private Hashtable<String,String> compTable;
        private Hashtable<String,String> jumpTable;
        
        //making the constructor
        public Code() {
            this.destTable = new Hashtable<String, String>();
            this.initializationDestTable();
            this.compTable = new Hashtable<String, String>();
            this.initializationCompTable();
            this.jumpTable = new Hashtable<String, String>();
            this.initializationJumpTable();
        }
        //the dictionary init
        private void initializationJumpTable() {
            this.jumpTable.put("NULL", "000");
            this.jumpTable.put("JGT", "001");
            this.jumpTable.put("JEQ", "010");
            this.jumpTable.put("JGE", "011");
            this.jumpTable.put("JLT", "100");
            this.jumpTable.put("JNE", "101");
            this.jumpTable.put("JLE", "110");
            this.jumpTable.put("JMP", "111");
        }

        private void initializationCompTable() {
            this.compTable.put("0", "0101010");
            this.compTable.put("1", "0111111");
            this.compTable.put("-1", "0111010");
            this.compTable.put("D", "0001100");
            this.compTable.put("A", "0110000");
            this.compTable.put("M", "1110000");
            this.compTable.put("!D", "0001101");
            this.compTable.put("!A", "0110001");
            this.compTable.put("!M", "1110001");
            this.compTable.put("-D", "0001111");
            this.compTable.put("-A", "0110011");
            this.compTable.put("-M", "1110011");
            this.compTable.put("D+1", "0011111");
            this.compTable.put("A+1", "0110111");
            this.compTable.put("M+1", "1110111");
            this.compTable.put("D-1", "0001110");
            this.compTable.put("A-1", "0110010");
            this.compTable.put("M-1", "1110010");
            this.compTable.put("D+A", "0000010");
            this.compTable.put("D+M", "1000010");
            this.compTable.put("D-A", "0010011");
            this.compTable.put("D-M", "1010011");
            this.compTable.put("A-D", "0000111");
            this.compTable.put("M-D", "1000111");
            this.compTable.put("D&A", "0000000");
            this.compTable.put("D&M", "1000000");
            this.compTable.put("D|A", "0010101");
            this.compTable.put("D|M", "1010101");
        }

        private void initializationDestTable() {
            this.destTable.put("NULL", "000");
            this.destTable.put("M", "001");
            this.destTable.put("D", "010");
            this.destTable.put("MD", "011");
            this.destTable.put("A", "100");
            this.destTable.put("AM", "101");
            this.destTable.put("AD", "110");
            this.destTable.put("AMD", "111");
        }

        public String binary(String input) {
            int number = Integer.parseInt(input);
            String inBinary = Integer.toBinaryString(number);
            String str = "";
            for(int i = 0;i < 15 - inBinary.length(); i++) {
                str += "0";
            }
            String completeBinary = str + inBinary;
            return completeBinary;
        }

        // return the jump from the dictionaries
        public String jump(String key) {
            if (key == null || key.isEmpty()) {
                key = "NULL";
            }

            return this.jumpTable.get(key);
        }
        
        // return the comp from the dictionaries
        public String comp(String key) {
            return this.compTable.get(key);
        }
        
        // return the destination from the dictionaries
        public String dest(String key) {
            if (key == null || key.isEmpty()) {
                key = "NULL";
            }
            return this.destTable.get(key);
        }
        
        // to string function
        public String toString()
        {
            return this.destTable.toString() + '\n' + this.destTable.toString() + '\n' + this.jumpTable.toString() ;
        }
    }
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
