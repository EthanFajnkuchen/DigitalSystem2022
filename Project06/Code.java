import java.nio.charset.StandardCharsets;
import java.util.*;

public class Code {
    private static Hashtable<String,String> destTable;
    private static Hashtable<String,String> compTable;
    private static Hashtable<String,String> jumpTable;

    public Code() {
        this.destTable = new Hashtable<String, String>();
        this.initializationDestTable();
        this.compTable = new Hashtable<String, String>();
        this.initializationCompTable();
        this.jumpTable = new Hashtable<String, String>();
        this.initializationJumpTable();
    }

    private static void initializationJumpTable() {
        jumpTable.put("NULL", "000");
        jumpTable.put("JGT", "001");
        jumpTable.put("JEQ", "010");
        jumpTable.put("JGE", "011");
        jumpTable.put("JLT", "100");
        jumpTable.put("JNE", "101");
        jumpTable.put("JLE", "110");
        jumpTable.put("JMP", "111");
    }

    private static void initializationCompTable() {
        compTable.put("0", "0101010");
        compTable.put("1", "0111111");
        compTable.put("-1", "0111010");
        compTable.put("D", "0001100");
        compTable.put("A", "0110000");
        compTable.put("M", "1110000");
        compTable.put("!D", "0001101");
        compTable.put("!A", "0110001");
        compTable.put("!M", "1110001");
        compTable.put("-D", "0001111");
        compTable.put("-A", "0110011");
        compTable.put("-M", "1110011");
        compTable.put("D+1", "0011111");
        compTable.put("A+1", "0110111");
        compTable.put("M+1", "1110111");
        compTable.put("D-1", "0001110");
        compTable.put("A-1", "0110010");
        compTable.put("M-1", "1110010");
        compTable.put("D+A", "0000010");
        compTable.put("D+M", "1000010");
        compTable.put("D-A", "0010011");
        compTable.put("D-M", "1010011");
        compTable.put("A-D", "0000111");
        compTable.put("M-D", "1000111");
        compTable.put("D&A", "0000000");
        compTable.put("D&M", "1000000");
        compTable.put("D|A", "0010101");
        compTable.put("D|M", "1010101");
    }

    private static void initializationDestTable() {
        destTable.put("NULL", "000");
        destTable.put("M", "001");
        destTable.put("D", "010");
        destTable.put("MD", "011");
        destTable.put("A", "100");
        destTable.put("AM", "101");
        destTable.put("AD", "110");
        destTable.put("AMD", "111");
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


    public static String jump(String key) {
        initializationJumpTable();
        if (key == null || key.isEmpty()) {
            key = "NULL";
        }
        String out = jumpTable.get(key);
        return out;
    }

    public static String comp(String key) {
        initializationCompTable();
        String out = compTable.get(key);
        return out;
    }

    public static String dest(String key) {
        initializationDestTable();
        if (key == null || key.isEmpty()) {
            key = "NULL";
        }
        String out = destTable.get(key);
        return out;
    }
}
