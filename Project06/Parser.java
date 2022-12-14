import java.io.*;

public class Parser {
    private static final int COMMAND_A = 1;
    private static final int COMMAND_C = 2;
    private static final int COMMAND_L = 3;//label


    public BufferedReader bfrReader;
    public String current;
    public String next;

    //making a constructor
    public Parser(File input) throws IOException  {
        this.bfrReader = new BufferedReader(new FileReader(input));
        this.current = null;
        this.next = this.readNextLine();
    }

    // check if we start with "//"
    public boolean comment(String input) {
        boolean isComment = false;
        isComment = input.trim().startsWith("//");
        return isComment;
    }

    // check if there is more line
    public boolean hasMoreLine() {
        if (this.next != null) {return true;}
        return false;
    }
    public void closebuff() throws IOException {
        bfrReader.close();
    }
    public BufferedReader getBufferedReader()
    {
        BufferedReader buff = this.bfrReader;
        return buff;
    }
    public String getCurrent()
    {
        String cur = this.current;
        return cur;
    }
    public String getNext()
    {
        String next = this.next;
        return next;
    }
    // reading the next line
    private String readNextLine() throws IOException {
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

    //continue to read
    public void advance() throws IOException {
        this.current = this.next;
        this.next = this.readNextLine();
    }

    // returning the desired command
    private int instructionType() {
        String line = this.current.trim();
        if (line.startsWith("(") && line.endsWith(")")) {return COMMAND_L; }
        if (line.startsWith("@")) { return COMMAND_A;}
        return COMMAND_C;
    }
    // returning the symbol 
    public String symbol() {
        String line = this.current.trim();
        if (this.instructionType() == COMMAND_L) { return line.substring(1,this.current.length() - 1); }
        if (this.instructionType() == COMMAND_A) { return line.substring(1);}
        return null;
    }

    // returning the destinations
    public String dest() {
        String line = this.current.trim();
        if (line.indexOf("=") == -1) {
            return null;
        } else {
            return line.substring(0,line.indexOf("="));
        }
    }

    // returning the comp
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

    // returning the jump
    public String jump() {
        String line = this.current.trim();
        if (line.indexOf(";") == -1) {
            return null;
        } else {
            return line.substring(line.indexOf(";") + 1);
        }
    }
}
