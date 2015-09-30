package uk.ac.glasgow.whitespace4j.imf;

import uk.ac.glasgow.whitespace4j.FiniteStateMachine;
import uk.ac.glasgow.whitespace4j.InterpretWhitespaceException;
import uk.ac.glasgow.whitespace4j.State;
import uk.ac.glasgow.whitespace4j.WhitespaceProgram;

public class InstructionModificationParameterTabState extends State {

	private State arithmeticState;
	private State ioState;
	private State heapState;
		
	public InstructionModificationParameterTabState(
		WhitespaceProgram program,
		FiniteStateMachine finiteStateMachine,
		State arithmeticState,
		State ioState,
		State heapState) {
		
		super(program , finiteStateMachine);
		this.arithmeticState = arithmeticState;
		this.ioState = ioState;
		this.heapState = heapState;
	}

	@Override
	protected void doLineFeedAction() throws InterpretWhitespaceException {
		logger.debug("Instruction modification: IO");
		ioState.execute();

	}

	@Override
	protected void doSpaceAction() throws InterpretWhitespaceException {
		logger.debug("Instruction modification: Arithmetic");
		arithmeticState.execute();

	}

	@Override
	protected void doTabAction() throws InterpretWhitespaceException {
		logger.debug("Instruction modification: Heap");
		heapState.execute();
	}

}
