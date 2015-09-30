package uk.ac.glasgow.whitespace4j.imf;

import uk.ac.glasgow.whitespace4j.FiniteStateMachine;
import uk.ac.glasgow.whitespace4j.InterpretWhitespaceException;
import uk.ac.glasgow.whitespace4j.State;
import uk.ac.glasgow.whitespace4j.WhitespaceProgram;

/**
 * Begin state for each whitespace instruction.
 * @author tws
 *
 */
public class InstructionModificationParameterState extends State {
	
	private State stackState;
	private State flowState;
	private State imfTab;
	
	public InstructionModificationParameterState(
		WhitespaceProgram program,
		FiniteStateMachine finiteStateMachine,
		State stackState,
		State flowState,
		State imfTab){
		
		super(program, finiteStateMachine);
		this.stackState = stackState;
		this.flowState = flowState;
		this.imfTab = imfTab;
	}

	public void execute() throws InterpretWhitespaceException{
		FiniteStateMachine finiteStateMachine =
			getFiniteStateMachine();

		finiteStateMachine.resetCurrentInstruction();
		super.execute();
	}
	
	@Override
	protected void doLineFeedAction() throws InterpretWhitespaceException{
		logger.debug("Instruction modification: Flow");
		flowState.execute();
	}

	@Override
	protected void doSpaceAction() throws InterpretWhitespaceException {
		logger.debug("Instruction modification: Stack");
		stackState.execute();
	}

	@Override
	protected void doTabAction() throws InterpretWhitespaceException{
		imfTab.execute();
	}

}
