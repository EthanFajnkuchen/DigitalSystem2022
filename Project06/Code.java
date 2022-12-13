import java.nio.charset.StandardCharsets;
import java.util.*;

public class Code {
    private Hashtable<String,String> destTable;
    private Hashtable<String,String> compTable;
    private Hashtable<String,String> jumpTable;

    public Code() {
        this.destTable = new Hashtable<String, String>();
        this.initializationDestTable();
        this.compTable = new Hashtable<String, String>();
        this.initalizationCompTable();
        this.jumpTable = new Hashtable<String, String>();
        this.initializationJumpTable();
    }

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

    private void initalizationCompTable() {
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


    public String jump(String key) {
        if (key == null || key.isEmpty()) {
            key = "NULL";
        }

        return this.jumpTable.get(key);
    }

    public String comp(String key) {
        return this.compTable.get(key);
    }

    public String dest(String key) {
        if (key == null || key.isEmpty()) {
            key = "NULL";
        }
        return this.destTable.get(key);
    }
}
