package uk.ac.glasgow.whitespace4j.stack;

import java.util.Stack;

import uk.ac.glasgow.whitespace4j.FiniteStateMachine;
import uk.ac.glasgow.whitespace4j.InterpretWhitespaceException;
import uk.ac.glasgow.whitespace4j.State;
import uk.ac.glasgow.whitespace4j.WhitespaceProgram;

public class StackTabState extends State{
	
	private Stack<Long> stack;
	
	public StackTabState(
		WhitespaceProgram program,
		FiniteStateMachine finiteStateMachine,
		Stack<Long> stack) {
		
		super(program, finiteStateMachine);
		
		this.stack = stack;
	}

	@Override
	protected void doLineFeedAction() throws InterpretWhitespaceException {
		Long n = interpretSignedNumber();

		if(getFiniteStateMachine().isInScanMode()) return;
		logger.debug("Sliding "+n+" elements of stack "+stack+".");

		Long e1 = stack.pop();
		
		while (n > 0){
			stack.pop();
			n--;
		}
		stack.push(e1);
	}

	@Override
	protected void doSpaceAction() throws InterpretWhitespaceException {
		Long index = interpretSignedNumber();
		
		if (getFiniteStateMachine().isInScanMode()) return;
		
		logger.debug("Copying ["+index+"th] element of stack "+stack+".");

		Long n = new Long(stack.elementAt(index.intValue()));
		stack.push(n);	
	}
}
