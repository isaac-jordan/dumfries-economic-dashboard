package uk.ac.glasgow.whitespace4j.stack;

import java.util.Stack;

import uk.ac.glasgow.whitespace4j.FiniteStateMachine;
import uk.ac.glasgow.whitespace4j.InterpretWhitespaceException;
import uk.ac.glasgow.whitespace4j.State;
import uk.ac.glasgow.whitespace4j.WhitespaceProgram;

public class StackLineFeedState extends State {
	
	private Stack<Long> stack;
	
	public StackLineFeedState(
		WhitespaceProgram program, 
		FiniteStateMachine finiteStateMachine, 
		Stack<Long> stack) {
		
		super(program, finiteStateMachine);
		this.stack = stack;
	}

	@Override
	protected void doLineFeedAction() throws InterpretWhitespaceException {
		if (getFiniteStateMachine().isInScanMode()) return;
		logger.debug("Popping the top of the stack "+stack+".");
		stack.pop();
	}

	@Override
	protected void doSpaceAction() throws InterpretWhitespaceException {
		if (getFiniteStateMachine().isInScanMode()) return;
		logger.debug("Copying top stack element "+stack+".");
		stack.push(
				new Long(
						stack.peek()
						));
		logger.debug("Copied top stack element "+stack+".");
	}

	@Override
	protected void doTabAction() throws InterpretWhitespaceException {
		if (getFiniteStateMachine().isInScanMode()) return;
		logger.debug("Switching top stack elements.");
		Long e1 = stack.pop();
		Long e2 = stack.pop();
		stack.push(e1);
		stack.push(e2);	
	}
}
