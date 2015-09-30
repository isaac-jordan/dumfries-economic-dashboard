package uk.ac.glasgow.whitespace4j.flow;

import java.util.Map;
import java.util.Stack;

import uk.ac.glasgow.whitespace4j.FiniteStateMachine;
import uk.ac.glasgow.whitespace4j.InterpretWhitespaceException;
import uk.ac.glasgow.whitespace4j.State;
import uk.ac.glasgow.whitespace4j.WhitespaceProgram;

public class FlowTabState extends State{
	
	private Stack<Long> stack;

	private Map<Long, Long> labels;
	
	private Stack<Long> subRoutines;
	
	public FlowTabState(
		WhitespaceProgram program,
		FiniteStateMachine finiteStateMachine,
		Stack<Long> stack,
		Map<Long,Long> labels,
		Stack<Long> subRoutines) {
		
		super(program, finiteStateMachine);
		
		this.stack = stack;
		this.labels = labels;
		this.subRoutines = subRoutines;
	}
	
	@Override
	protected void doLineFeedAction() throws InterpretWhitespaceException {
		if (getFiniteStateMachine().isInScanMode()) return;		
		
		Long lastPosition = subRoutines.pop();
		
		WhitespaceProgram program = getProgram();
		
		Long currentPosition = program.getCounter();
		
		String message = 
			"Returning from end of sub-routine at position [%s] to position [%s].";
		
		logger.debug(String.format(message, currentPosition, lastPosition));
		
		program.jump(lastPosition);
	}

	@Override
	protected void doSpaceAction() throws InterpretWhitespaceException {
		
		Long label = interpretUnsignedNumber();
		
		if (getFiniteStateMachine().isInScanMode()) return;
		
		WhitespaceProgram program = getProgram();
		
		Long condition = stack.pop();
		Long position = labels.get(label);
		
		String message =
				"Doing conditional 0=[%s] jump to label [%s] referencing position [%s].";
			
		logger.debug(String.format(message, condition, label, position));
			
		if (condition==0) program.jump(position);
	}

	@Override
	protected void doTabAction() throws InterpretWhitespaceException {
		
		Long label = interpretUnsignedNumber();
		
		if (getFiniteStateMachine().isInScanMode()) return;
		
		WhitespaceProgram program = getProgram();
		
		Long position = labels.get(label);
		Long condition = stack.pop();
		
		String message =
			"Doing conditional [%s]<0 jump to label [%s] referencing position [%s].";
		
		logger.debug(String.format(message, condition, label, position));
		
		if (condition<0) program.jump(position);
	}
}
