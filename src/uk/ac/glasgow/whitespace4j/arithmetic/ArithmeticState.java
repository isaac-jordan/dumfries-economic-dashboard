package uk.ac.glasgow.whitespace4j.arithmetic;

import uk.ac.glasgow.whitespace4j.FiniteStateMachine;
import uk.ac.glasgow.whitespace4j.InterpretWhitespaceException;
import uk.ac.glasgow.whitespace4j.State;
import uk.ac.glasgow.whitespace4j.WhitespaceProgram;

public class ArithmeticState extends State {
	
	private State arithmeticSpace;
	private State arithmeticTab;
	
	public ArithmeticState(
			WhitespaceProgram program,
			FiniteStateMachine finiteStateMachine,
			State arithmeticSpace,
			State arithmeticTab) {
		
		super(program, finiteStateMachine);
		this.arithmeticSpace = arithmeticSpace;
		this.arithmeticTab = arithmeticTab;
	}

	@Override
	protected void doSpaceAction() throws InterpretWhitespaceException {
		arithmeticSpace.execute();
	}

	@Override
	protected void doTabAction() throws InterpretWhitespaceException {
		arithmeticTab.execute();
	}

}
