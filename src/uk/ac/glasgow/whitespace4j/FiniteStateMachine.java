package uk.ac.glasgow.whitespace4j;

import java.io.BufferedReader;
import java.io.PrintWriter;

/**
 * Specifies public functions for a (reasonably) general purpose finite state machine.
 * @author tws
 *
 */
public interface FiniteStateMachine {

	public abstract boolean isInScanMode();

	public abstract void setInScanMode(boolean scanMode);

	public abstract BufferedReader getBufferedReader();

	public abstract PrintWriter getPrintWriter();

	/**
	 * Processes the next whitespace program instruction, beginning at the
	 * current program counter position.
	 */
	public abstract void executeNextInstruction();

	/**
	 * Adds the specified token to the sequence of tokens read so far for the
	 * current instruction.
	 * 
	 * @param token
	 */
	public abstract void addTokenToCurrentInstruction(Character token);

	/**
	 * @return the tokens of the current instruction that have been read so far.
	 */
	public abstract String getCurrentInstruction();

	/**
	 * Clears the sequence of tokens read for the current instruction.
	 */
	public abstract void resetCurrentInstruction();

	/**
	 * @return the set of three whitespace characters used for program
	 *         instructions.
	 */
	public abstract CharacterSet getCharacterSet();

}