package uk.ac.glasgow.whitespace4j;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.Map;
import java.util.Stack;

import org.apache.log4j.Logger;

import uk.ac.glasgow.whitespace4j.factory.StateFactory;

public class WhitespaceFSM implements FiniteStateMachine {
	
	protected static final Logger logger = Logger.getLogger(WhitespaceFSM.class);
	
	private boolean inScanMode;
	
	private State impState;
	
	private String currentInstruction;
	
	private BufferedReader bufferedReader;
	
	private PrintWriter printWriter;

	private CharacterSet characterSet;
	
	private WhitespaceProgram program;
	
	public WhitespaceFSM(
		WhitespaceProgram program,
		Interpreter interpreter,
		CharacterSet characterSet,
		InputStream inputStream,
		OutputStream outputStream){
		
		this.program = program;
		
		if (inputStream!=null)
			bufferedReader = 
				new BufferedReader(new InputStreamReader(inputStream));
		
		printWriter = new PrintWriter(outputStream);

		this.characterSet = characterSet;
		
		Map<Long,Long> heap = new HashMap<Long,Long>();
		Stack<Long> stack = new Stack<Long>();
		Map<Long,Long> labels = new HashMap<Long,Long>();		
		Stack<Long> subRoutines = new Stack<Long>();
		
		this.impState =
			StateFactory.createIMPState(
				program, this, interpreter, heap, stack, labels, subRoutines);
		
		resetCurrentInstruction();
	}
	
	/* (non-Javadoc)
	 * @see uk.ac.glasgow.senotes.whitespace.IFiniteStateMachine#isInScanMode()
	 */
	@Override
	public boolean isInScanMode() {
		return inScanMode;
	}

	/* (non-Javadoc)
	 * @see uk.ac.glasgow.senotes.whitespace.IFiniteStateMachine#setInScanMode(boolean)
	 */
	@Override
	public void setInScanMode(boolean scanMode) {
		this.inScanMode = scanMode;
	}
	
	/* (non-Javadoc)
	 * @see uk.ac.glasgow.senotes.whitespace.IFiniteStateMachine#getBufferedReader()
	 */
	@Override
	public BufferedReader getBufferedReader() {
		return bufferedReader;
	}

	/* (non-Javadoc)
	 * @see uk.ac.glasgow.senotes.whitespace.IFiniteStateMachine#getPrintWriter()
	 */
	@Override
	public PrintWriter getPrintWriter() {
		return printWriter;
	}
	
	/* (non-Javadoc)
	 * @see uk.ac.glasgow.senotes.whitespace.IFiniteStateMachine#executeNextInstruction()
	 */
	@Override
	public void executeNextInstruction() {
		try {
			impState.execute();	
		} catch (InterpretWhitespaceException e) {
			logger.fatal("Interpretation error at position ["+ program.getCounter() +"].", e);
		}
	}
	
	/* (non-Javadoc)
	 * @see uk.ac.glasgow.senotes.whitespace.IFiniteStateMachine#addTokenToCurrentInstruction(java.lang.Character)
	 */
	@Override
	public void addTokenToCurrentInstruction(Character token) {
		this.currentInstruction += token;
	}
	
	/* (non-Javadoc)
	 * @see uk.ac.glasgow.senotes.whitespace.IFiniteStateMachine#getCurrentInstruction()
	 */
	@Override
	public String getCurrentInstruction(){
		return this.currentInstruction;
	}
	
	/* (non-Javadoc)
	 * @see uk.ac.glasgow.senotes.whitespace.IFiniteStateMachine#resetCurrentInstruction()
	 */
	@Override
	public void resetCurrentInstruction(){
		currentInstruction = "";
	}
	
	/* (non-Javadoc)
	 * @see uk.ac.glasgow.senotes.whitespace.IFiniteStateMachine#getCharacterSet()
	 */
	@Override
	public CharacterSet getCharacterSet() {
		return characterSet;
	}

}