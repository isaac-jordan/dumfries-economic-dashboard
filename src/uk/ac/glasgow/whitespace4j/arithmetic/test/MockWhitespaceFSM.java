package uk.ac.glasgow.whitespace4j.arithmetic.test;

import java.io.BufferedReader;
import java.io.PrintWriter;

import uk.ac.glasgow.whitespace4j.CharacterSet;
import uk.ac.glasgow.whitespace4j.FiniteStateMachine;

/**
 * Provides mock implementations of FiniteStateMachine operations to support
 * testing of individual states within a Whitespace finite state machine.
 * 
 * @author tws
 * 
 */
public class MockWhitespaceFSM implements FiniteStateMachine {

	private CharacterSet characterSet;
	
	public MockWhitespaceFSM(CharacterSet characterSet) {
		this.characterSet = characterSet;
	}

	@Override
	public boolean isInScanMode() {
		return false;
	}

	@Override
	public void setInScanMode(boolean scanMode) {
	}

	@Override
	public BufferedReader getBufferedReader() {
		return null;
	}

	@Override
	public PrintWriter getPrintWriter() {
		return null;
	}

	@Override
	public void executeNextInstruction() {	}

	@Override
	public void addTokenToCurrentInstruction(Character token) {}

	@Override
	public String getCurrentInstruction() {
		return null;
	}

	@Override
	public void resetCurrentInstruction() {
	}

	@Override
	public CharacterSet getCharacterSet() {
		return characterSet;
	}
}
