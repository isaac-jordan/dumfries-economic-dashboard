package uk.ac.glasgow.whitespace4j;

import java.io.InputStream;
import java.io.OutputStream;

import org.apache.log4j.Logger;

public class Interpreter   {
	
	protected static final Logger logger = Logger.getLogger(Interpreter.class);
			
	private Boolean halt = false;
	
	private FiniteStateMachine finiteStateMachine;
		
	public Interpreter (WhitespaceProgram program, CharacterSet characterSet, InputStream in, OutputStream out){
		
		finiteStateMachine = 
			new WhitespaceFSM(program, this, characterSet, in, out);
				
		finiteStateMachine.setInScanMode(true);		
				
		logger.debug("Beginning scan of labels.");
		
		while (!program.isAtEnd())
			finiteStateMachine.executeNextInstruction();
		
		logger.debug("Completed scan of labels");

		finiteStateMachine.setInScanMode(false);
		program.reset();		
	}
	
	public void run (){
		
		while(!halt)				
			finiteStateMachine.executeNextInstruction();			
	}
	
	public void halt(){
		halt = true;
	}
}
