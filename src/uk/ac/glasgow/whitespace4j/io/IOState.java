package uk.ac.glasgow.whitespace4j.io;

import uk.ac.glasgow.whitespace4j.FiniteStateMachine;
import uk.ac.glasgow.whitespace4j.InterpretWhitespaceException;
import uk.ac.glasgow.whitespace4j.State;
import uk.ac.glasgow.whitespace4j.WhitespaceProgram;

public class IOState extends State {
	
	private State input;
	private State output;
	
	public IOState(
		WhitespaceProgram program, 
		FiniteStateMachine finiteStateMachine, 
		State input, 
		State output) {
		
		super(program, finiteStateMachine);
		this.input = input;
		this.output = output;
	}

	@Override
	protected void doSpaceAction() throws InterpretWhitespaceException {
		output.execute();
		
	}

	@Override
	protected void doTabAction() throws InterpretWhitespaceException {
		input.execute();
	}
	
}
