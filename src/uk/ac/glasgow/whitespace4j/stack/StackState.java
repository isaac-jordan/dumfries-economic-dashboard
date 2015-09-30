package uk.ac.glasgow.whitespace4j.stack;

import java.util.Stack;

import org.apache.log4j.Logger;

import uk.ac.glasgow.whitespace4j.FiniteStateMachine;
import uk.ac.glasgow.whitespace4j.InterpretWhitespaceException;
import uk.ac.glasgow.whitespace4j.State;
import uk.ac.glasgow.whitespace4j.WhitespaceProgram;

public class StackState extends State{
	
	private static final Logger logger = Logger.getLogger(StackState.class);
	
	private Stack<Long> stack;
	
	private State stack_ta;
	private State stack_lf;
	
	public StackState(
		WhitespaceProgram program,
		FiniteStateMachine finiteStateMachine,
		Stack<Long> stack, 
		State stack_lf, 
		State stack_ta) {
		
		super(program, finiteStateMachine);
		this.stack = stack;
		this.stack_ta = stack_ta;
		this.stack_lf = stack_lf;
	}

	@Override
	protected void doLineFeedAction() throws InterpretWhitespaceException {
		stack_lf.execute();
		
	}

	@Override
	protected void doSpaceAction() throws InterpretWhitespaceException {
		
		Long i = interpretSignedNumber();
		
		if(getFiniteStateMachine().isInScanMode())return;
		
		logger.debug("Adding number ["+i+"] to stack "+ stack+"." );
		
		stack.push(i);
	}

	@Override
	protected void doTabAction() throws InterpretWhitespaceException {
		stack_ta.execute();
	}
	
}
