package uk.ac.glasgow.whitespace4j.io;

import java.util.Stack;

import org.apache.log4j.Logger;

import uk.ac.glasgow.whitespace4j.FiniteStateMachine;
import uk.ac.glasgow.whitespace4j.InterpretWhitespaceException;
import uk.ac.glasgow.whitespace4j.State;
import uk.ac.glasgow.whitespace4j.WhitespaceProgram;

public class OutputState extends State {
	
	private static final Logger logger = Logger.getLogger(OutputState.class);

	
	private Stack<Long> stack;
	
	public OutputState(
		WhitespaceProgram program,
		FiniteStateMachine finiteStateMachine,
		Stack<Long> stack) {
		
		super(program, finiteStateMachine);
		this.stack = stack;
	}

	@Override
	protected void doSpaceAction() throws InterpretWhitespaceException {
		
		FiniteStateMachine machine = 
				getFiniteStateMachine();
		
		if (machine.isInScanMode()) return;
		
		logger.debug(
			"Outputing value ["+stack.peek().intValue()+"] on top of stack "+stack+".");
		
		int value = stack.pop().intValue();
		
		machine.getPrintWriter().write((char)value);
		machine.getPrintWriter().flush();
		
	}

	@Override
	protected void doTabAction() throws InterpretWhitespaceException {
		
		FiniteStateMachine machine = 
				getFiniteStateMachine();
		
		if (machine.isInScanMode()) return;

		int value = stack.pop().intValue();	 

		logger.debug(
			"Outputing value ["+value+"] popped from stack "+stack+".");
		
		machine.getPrintWriter().print(value);
		machine.getPrintWriter().flush();
	}

}
