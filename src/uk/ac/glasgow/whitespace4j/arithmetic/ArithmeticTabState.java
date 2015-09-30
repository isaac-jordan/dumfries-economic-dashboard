package uk.ac.glasgow.whitespace4j.arithmetic;

import uk.ac.glasgow.whitespace4j.FiniteStateMachine;
import uk.ac.glasgow.whitespace4j.InterpretWhitespaceException;
import uk.ac.glasgow.whitespace4j.State;
import uk.ac.glasgow.whitespace4j.WhitespaceProgram;

public class ArithmeticTabState extends State{
	
	private ArithmeticUnit arithmeticUnit;
	
	public ArithmeticTabState(
		WhitespaceProgram program,
		FiniteStateMachine finiteStateMachine,
		ArithmeticUnit arithmeticUnit) {
		super(program, finiteStateMachine);
		this.arithmeticUnit = arithmeticUnit;
	}

	@Override
	protected void doSpaceAction() throws InterpretWhitespaceException {
		if (getFiniteStateMachine().isInScanMode()) return;
		try {
			this.arithmeticUnit.doOperation(OpFlag.DIVISION);
		} catch (Exception e) {
			throw new InterpretWhitespaceException(getProgram(), this, e);
		}
	}

	@Override
	protected void doTabAction() throws InterpretWhitespaceException {
		if (getFiniteStateMachine().isInScanMode()) return;
		try {
			this.arithmeticUnit.doOperation(OpFlag.MODULO);
		} catch (Exception e) {
			throw new InterpretWhitespaceException(getProgram(), this, e);
		}
	}
}