package uk.ac.glasgow.whitespace4j.io;

import java.io.IOException;
import java.util.Map;
import java.util.Stack;

import uk.ac.glasgow.whitespace4j.FiniteStateMachine;
import uk.ac.glasgow.whitespace4j.InterpretWhitespaceException;
import uk.ac.glasgow.whitespace4j.State;
import uk.ac.glasgow.whitespace4j.WhitespaceProgram;

public class InputState extends State{
	
	private Stack<Long> stack;
	private Map<Long,Long> heap;
		
	public InputState(
		WhitespaceProgram program,
		FiniteStateMachine finiteStateMachine,
		Stack<Long> stack,
		Map<Long,Long> heap) {
		
		super(program, finiteStateMachine);
		this.stack = stack;
		this.heap = heap;
	}

	@Override
	protected void doSpaceAction() throws InterpretWhitespaceException {
		
		FiniteStateMachine machine = 
			getFiniteStateMachine();
		
		try {
			if(machine.isInScanMode())return;
			char input = (char)machine.getBufferedReader().read();
			heap.put( stack.peek(), (long)input);
		} catch (IOException e) {
			e.printStackTrace();
		}	
	}

	@Override
	protected void doTabAction() throws InterpretWhitespaceException {
		
		FiniteStateMachine machine = 
				getFiniteStateMachine();
		
		try {
			if(machine.isInScanMode())return;
			Long input = Long.parseLong(machine.getBufferedReader().readLine());
			heap.put(stack.peek(), input);
		} catch (IOException e) {
			e.printStackTrace();
		}		
	}

}