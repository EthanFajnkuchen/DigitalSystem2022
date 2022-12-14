
/**
 * HackAssembler.Java
 *
 * @author Franklin Ogidi
 *
 * @description Drives the process of translating code written in the Hack assembly
 * language into machine code, according to the Hack Language specifications.
 * This program was written as part of the NandToTetris course: https://www.nand2tetris.org/project06
 *
 * @version 1.0
 *
 */

import java.io.*;
import java.util.*;

public class HackAssembler {
    private final SymbolTable symbols;  // stores pre-defined and user-defined symbols and labels
    private int current_line;           // keeps track of the current valid line during file I/O
    private Parser parser;              // parses Hack Assembly commands into individual parts

    // constructor
    public HackAssembler() {
        symbols = new SymbolTable();
        current_line = 0;
    } // end constructor

    /**
     * Performs the first pass on the file specified by filename, noting only the
     * labels. Adds label to the SymbolTable only at the first occurrence.
     *
     * @param filename The .asm file to parse.
     */

    /**
     * Performs the first pass on the file specified by filename, noting only the
     * labels. Adds label to the SymbolTable only at the first occurrence.
     *
     * @param filename The .asm file to parse.
     */
    private void first_pass(final String filename) {
        try {
            boolean parse_success; // flag for parse error
            File file = new File(filename);
            this.parser = new Parser(file);
            while (parser.hasMoreLine()) {
                String line = parser.getCurrent();
                parse_success = parser.comment(line);
                if (parse_success) {
                    if (line.trim().charAt(0) == '(') { // checking for labels [ eg. (LABEL) ]

                        // extract the label's symbol
                        final String symbol = parser.symbol();

                        // add label to SymbolTable if it is not already present
                        symbols.addEntry(symbol,this.current_line);
                        this.current_line -- ;
                    }
                    this.current_line ++;
                }
                this.parser.advance();
            }
        } catch (final IOException ioe) {
            System.out.println(ioe);
            return;
        }
    } // end first pass

    /**
     * Translates a Hack Assembly file (.asm) into machine code (.hack file)
     * according to the Hack Machine Language specifications, after the first pass.
     *
     * @param filename The assembly file to translate into machine code
     */
    private void translate(final String filename) {
        try {
            final String output_filename = filename.substring(0, filename.indexOf(".")) + ".hack"; // change file
            // extension from
            // .asm to .hack
            File file = new File(filename);
            this.parser = new Parser(file);
            final PrintWriter output = new PrintWriter(output_filename);
            this.current_line =0; // reset counter for current line
            boolean parse_success; // flag for parsing error

            while (this.parser.hasMoreLine()) {
                String line = this.parser.getCurrent();
                parse_success = this.parser.comment(this.parser.getCurrent());
                if (parse_success && line.trim().charAt(0) != '(') { // label declarations don't count
                    if (this.parser.symbol() == null) { // parsing a C-instruction
                        final String comp = Code.comp(this.parser.comp());
                        final String dest = Code.dest(this.parser.dest());
                        final String jump = Code.jump(this.parser.jump());
                        output.printf("111" + comp + dest + jump);
                    } else { // parsing an A-instruction
                        final String var = this.parser.symbol();

                        final Scanner sc = new Scanner(var);
                        if (sc.hasNextInt()) { // check if var is an integer
                            final String addr_binary = Integer.toBinaryString(Integer.parseInt(var)); // convert to
                            // binary
                            output.println(pad_binary(addr_binary)); // write 16-bit binary to output
                        } else {
                            symbols.addEntry(var, symbols.getRegiserNum());
                            final String addr_binary = Integer.toBinaryString(symbols.getAddress(var));
                            output.println(pad_binary(addr_binary));
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
    } // end translate
    /**
     * Pads a binary String with zeros to ensure 16-bit binary format
     *
     * @param unpadded_binary The binary String without leading zeros
     * @return A 16-bit binary String with leading zeros where necessary
     */
    private String pad_binary(final String unpadded_binary) {
        String padded_binary = "";
        final int num_zeros = 16 - unpadded_binary.length();

        for (int i = 0; i < num_zeros; i++) {
            padded_binary += "0";
        }

        return padded_binary + unpadded_binary;
    } // end pad_binary

    /**
     * Interface for running the Hack Assembler in the command line in the following
     * format: $ java HackAssembler filename
     *
     * @param args only the filename argument is supported
     */
    public static void main(final String[] args) {
        final String filename = args[0];
        final HackAssembler assembly = new HackAssembler();
        assembly.first_pass(filename);
        assembly.translate(filename);
    } // end main
} // end HackAssembler class
