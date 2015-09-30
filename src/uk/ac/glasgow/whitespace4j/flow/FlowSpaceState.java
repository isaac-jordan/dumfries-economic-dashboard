package uk.ac.glasgow.whitespace4j.flow;

import java.util.Map;
import java.util.Stack;

import uk.ac.glasgow.whitespace4j.FiniteStateMachine;
import uk.ac.glasgow.whitespace4j.InterpretWhitespaceException;
import uk.ac.glasgow.whitespace4j.State;
import uk.ac.glasgow.whitespace4j.WhitespaceProgram;

public class FlowSpaceState extends State {
		
	private Map<Long,Long> labels;
	
	private  Stack<Long> subRoutines;
	
	public FlowSpaceState(
		WhitespaceProgram program,
		FiniteStateMachine finiteStateMachine,
		Map<Long,Long> labels,
		Stack<Long> subRoutines
		) {
		
		super(program, finiteStateMachine);
		this.labels = labels;
		this.subRoutines = subRoutines;
	}

	@Override
	protected void doLineFeedAction() throws InterpretWhitespaceException {
		Long label = interpretUnsignedNumber();

		if (getFiniteStateMachine().isInScanMode()) return;
		
		Long position = labels.get(label);
		
		logger.debug("Doing unconditional jump to: "+position+" : from position: "+getProgram().getCounter()+".");
		
		getProgram().jump(position);
	}

	@Override
	protected void doSpaceAction() throws InterpretWhitespaceException {
		
		Long label = interpretUnsignedNumber();
		
		if (!getFiniteStateMachine().isInScanMode()) return;

		logger.debug("Found label ["+label+"] at position ["+getProgram().getCounter()+"].");
		labels.put(label,getProgram().getCounter());
	}

	@Override
	protected void doTabAction() throws InterpretWhitespaceException {
		Long label = interpretUnsignedNumber();
		
		FiniteStateMachine finiteStateMachine =
			getFiniteStateMachine();
		
		if (finiteStateMachine.isInScanMode()) return;

		Long labelPosition = labels.get(label);
		
		Long currentPosition = getProgram().getCounter();
		
		String currentInstruction = 
			finiteStateMachine.getCurrentInstruction();
		
		String message =
			"Calling sub-routine [%s] at position [%s] from position [%s] with instruction [%s].";

		logger.debug(
			String.format(message, label, labelPosition, currentPosition, currentInstruction));
		
		subRoutines.push(currentPosition);
		getProgram().jump(labelPosition);
	}

}
