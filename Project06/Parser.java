import java.io.*;

public class Parser {
    public static final int COMMAND_A = 1;
    public static final int COMMAND_C = 2;
    public static final int COMMAND_L = 3;


    private BufferedReader bfrReader;
    private String current;
    private String next;
    private int conmmandType;

    public Parser(File input) throws IOException  {
            this.bfrReader = new BufferedReader(new FileReader(input));
            this.current = null;
            this.next = this.readNextLine();
            this.conmmandType = 0;

    }

    private boolean comment(String input) {
        boolean isComment = false;
        isComment = input.trim().startsWith("//");
        return isComment;
    }
    public boolean hasMoreLine() {
        if (this.next != null) {return true;}
        return false;
    }

    public String readNextLine() throws IOException {
        try {
            String nextLine = "";
            nextLine = this.bfrReader.readLine();
            if (nextLine == null) {
                return null;
            }
            while (nextLine.trim().isEmpty() || this.comment(nextLine)) {
                nextLine = this.bfrReader.readLine();
                if (nextLine == null) {
                    return null;
                }
            }
            if (nextLine.indexOf("//") != -1) {
                nextLine = nextLine.substring(0, nextLine.indexOf("//") - 1);
            }

            return nextLine;
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }

    public void advance() throws IOException {
        this.current = this.next;
        this.next = this.readNextLine();
    }

    public int instructionType() {
        String line = this.current.trim();
        if (line.startsWith("(") && line.endsWith(")")) {return COMMAND_L; }
        if (line.startsWith("@")) { return COMMAND_A;}
        return COMMAND_C;
        }

    public String symbol() {
        String line = this.current.trim();
        if (this.instructionType() == COMMAND_L) { return line.substring(1,this.current.length() - 1); }
        if (this.instructionType() == COMMAND_A) { return line.substring(1);}
        return null;
    }

    public String dest() {
        String line = this.current.trim();
        if (line.indexOf("=") == -1) {
            return null;
        } else {
            return line.substring(0,line.indexOf("="));
        }
    }

    public String comp() {
        String line = this.current.trim();
        if (line.indexOf("=") == -1) {
            line = line.substring(line.indexOf("=") + 1);
        }

        if (line.indexOf(";") == -1) {
            return line;
        } else {
            return line.substring(0,line.indexOf(";"));
        }
    }

    public String jump() {
        String line = this.current.trim();
        if (line.indexOf(";") == -1) {
            return null;
        } else {
            return line.substring(line.indexOf(";") + 1);
        }
    }
}
