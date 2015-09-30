package uk.ac.glasgow.whitespace4j.heap;

import java.util.Map;
import java.util.Stack;

import uk.ac.glasgow.whitespace4j.FiniteStateMachine;
import uk.ac.glasgow.whitespace4j.InterpretWhitespaceException;
import uk.ac.glasgow.whitespace4j.State;
import uk.ac.glasgow.whitespace4j.WhitespaceProgram;

public class HeapState extends State {
		
	private Stack<Long> stack;

	private Map<Long,Long> heap;

	public HeapState(
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
				
		if (getFiniteStateMachine().isInScanMode())return;
		
		Long value = stack.pop();
		Long key = stack.pop();

		logger.debug(
			"Storing ["+value+"] at ["+key+"]. on heap "+heap+".");
		
		heap.put(key, value);
	}

	@Override
	protected void doTabAction() throws InterpretWhitespaceException {
		
		if (getFiniteStateMachine().isInScanMode())return;
		
		Long key = stack.pop();
		
		logger.debug(
			"retrieving value at key ["+key+"] from heap ["+heap+"].");
		
		stack.push(heap.get(key));
	}
}
