package uk.ac.glasgow.whitespace4j.flow;

import uk.ac.glasgow.whitespace4j.FiniteStateMachine;
import uk.ac.glasgow.whitespace4j.InterpretWhitespaceException;
import uk.ac.glasgow.whitespace4j.Interpreter;
import uk.ac.glasgow.whitespace4j.State;
import uk.ac.glasgow.whitespace4j.WhitespaceProgram;

public class FlowLineFeedState extends State {
	
	private Interpreter interpreter;
	
	public FlowLineFeedState(WhitespaceProgram program, FiniteStateMachine finiteStateMachine, Interpreter interpreter) {
		super(program, finiteStateMachine);
		this.interpreter = interpreter;
	}

	@Override
	protected void doLineFeedAction() throws InterpretWhitespaceException {
		if (getFiniteStateMachine().isInScanMode()) return;
		
		String message = "Halting at position [%s].";
		
		Long position = getProgram().getCounter();
		
		logger.debug(String.format(message, position));
		interpreter.halt();
	}
}
