import java.io.*;
import java.util.*;

public class HackAssembler {
    private final SymbolTable symbols;  // stores the SymbolTable
    private int current_line;           // the valid line
    private Parser parser;              // making a parser for the HackAssembly commands

    // making the constructor
    public HackAssembler() {
        symbols = new SymbolTable();
        current_line = 0;
    }
    
    // returning a binary String with length 16 whit zeros where we need
    private String ToBinary(final String NonBinary) {
        String IsBinary = "";
        int zero = 16 - NonBinary.length();

        for (int i = 0; i < zero; i++) {
            IsBinary += "0";
        }

        return IsBinary + NonBinary;
    }
    
    // Adds label to the SymbolTable only at the first meeting
    private void OnlyLabel(final String filename) {
        try {
            boolean isWorking; // if It's valid or not
            File file = new File(filename);
            this.parser = new Parser(file);
            while (parser.hasMoreLine()) {
                String line = parser.getCurrent();
                isWorking = parser.comment(line);
                if (isWorking) {
                    if (parser.IsItLabel()) { // if its label or not

                        String symbol = parser.symbol(); //returning the symbol
                        // add label's to SymbolTable
                        symbols.addEntry(symbol,this.current_line);
                        this.current_line -- ;
                    }
                    this.current_line ++;
                }
                this.parser.advance();
            }
        } catch (IOException e) {
            System.out.println(e);
            return;
        }
    } // end first pass

    // Translates a Hack Assembly file into machine code file (from .asm to .hack
    private void SwitchTranslate(String filename) {
        try {
            final String outfile = filename.substring(0, filename.indexOf(".")) + ".hack"; // change file
            File file = new File(filename);
            this.parser = new Parser(file);
            final PrintWriter output = new PrintWriter(outfile);
            this.current_line =0; // reset counter for current line
            boolean isWorking; // flag for parsing error

            while (this.parser.hasMoreLine()) {
                String line = this.parser.getCurrent();
                isWorking = this.parser.comment(this.parser.getCurrent());
                if (isWorking && !parser.IsItLabel()) { // what with label don't count
                    if (this.parser.symbol() == null) { // making the instructions
                        final String comp = Code.comp(this.parser.comp());
                        final String jump = Code.jump(this.parser.jump());
                        final String dest = Code.dest(this.parser.dest());
                        output.printf("111" + comp + dest + jump); // returning the 16 binary output
                    }
                    // making the A-instruction
                    else
                    {
                        final String var = this.parser.symbol();
                        final Scanner sc = new Scanner(var);
                        if (sc.hasNextInt()) { // check if var is an integer
                            String address = Integer.toBinaryString(Integer.parseInt(var)); // convert to binary
                            output.println(ToBinary(address)); // write as binary
                        } else {
                            symbols.addEntry(var, symbols.getRegisterNum());
                            String address = Integer.toBinaryString(symbols.getAddress(var));
                            output.println(ToBinary(address));
                        }
                        sc.close();
                    }
                }
                this.parser.advance();
            }
            this.parser.closebuff();
            output.close();
        } catch (final IOException ioe) {
            System.out.println(ioe);
            return;
        }
    }
    
    //the main program
    public static void main(String[] args) {
        String filename = args[0];
        HackAssembler hack = new HackAssembler();
        hack.OnlyLabel(filename);
        hack.SwitchTranslate(filename);
    }
}
