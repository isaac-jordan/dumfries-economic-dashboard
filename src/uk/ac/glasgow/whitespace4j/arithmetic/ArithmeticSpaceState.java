package uk.ac.glasgow.whitespace4j.arithmetic;

import uk.ac.glasgow.whitespace4j.FiniteStateMachine;
import uk.ac.glasgow.whitespace4j.InterpretWhitespaceException;
import uk.ac.glasgow.whitespace4j.State;
import uk.ac.glasgow.whitespace4j.WhitespaceProgram;

/**
 * State entered after a Tab, Space, Space sequence.
 * @author tws
 */
public class ArithmeticSpaceState extends State{
		
	private ArithmeticUnit arithmeticUnit;
	
	public ArithmeticSpaceState(
		WhitespaceProgram program,
		FiniteStateMachine finiteStateMachine,
		ArithmeticUnit arithmeticUnit) {
		super(program, finiteStateMachine);
		this.arithmeticUnit = arithmeticUnit;
	}

	@Override
	protected void doLineFeedAction() throws InterpretWhitespaceException {
		if (getFiniteStateMachine().isInScanMode()) return;
		try {
			arithmeticUnit.doOperation(OpFlag.MULTIPLICATION);
		} catch (Exception e) {
			throw new InterpretWhitespaceException(getProgram(), this);
		}
	}

	@Override
	protected void doSpaceAction() throws InterpretWhitespaceException {
		if (getFiniteStateMachine().isInScanMode()) return;
		try {
			arithmeticUnit.doOperation(OpFlag.ADDITION);
		} catch (Exception e) {
			throw new InterpretWhitespaceException(getProgram(), this, e);

		}
	}

	@Override
	protected void doTabAction() throws InterpretWhitespaceException {
		if (getFiniteStateMachine().isInScanMode()) return;
		try {
			arithmeticUnit.doOperation(OpFlag.SUBTRACTION);
		} catch (Exception e) {
			throw new InterpretWhitespaceException(getProgram(), this, e);
		}
	}
}