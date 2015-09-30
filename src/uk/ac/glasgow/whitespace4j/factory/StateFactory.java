package uk.ac.glasgow.whitespace4j.factory;

import java.util.Map;
import java.util.Stack;

import uk.ac.glasgow.whitespace4j.FiniteStateMachine;
import uk.ac.glasgow.whitespace4j.Interpreter;
import uk.ac.glasgow.whitespace4j.State;
import uk.ac.glasgow.whitespace4j.WhitespaceProgram;
import uk.ac.glasgow.whitespace4j.arithmetic.ArithmeticSpaceState;
import uk.ac.glasgow.whitespace4j.arithmetic.ArithmeticState;
import uk.ac.glasgow.whitespace4j.arithmetic.ArithmeticTabState;
import uk.ac.glasgow.whitespace4j.arithmetic.ArithmeticUnit;
import uk.ac.glasgow.whitespace4j.flow.FlowLineFeedState;
import uk.ac.glasgow.whitespace4j.flow.FlowSpaceState;
import uk.ac.glasgow.whitespace4j.flow.FlowState;
import uk.ac.glasgow.whitespace4j.flow.FlowTabState;
import uk.ac.glasgow.whitespace4j.heap.HeapState;
import uk.ac.glasgow.whitespace4j.imf.InstructionModificationParameterState;
import uk.ac.glasgow.whitespace4j.imf.InstructionModificationParameterTabState;
import uk.ac.glasgow.whitespace4j.io.IOState;
import uk.ac.glasgow.whitespace4j.io.InputState;
import uk.ac.glasgow.whitespace4j.io.OutputState;
import uk.ac.glasgow.whitespace4j.stack.StackLineFeedState;
import uk.ac.glasgow.whitespace4j.stack.StackState;
import uk.ac.glasgow.whitespace4j.stack.StackTabState;

public class StateFactory {
	
	public static State createIMPState(
			WhitespaceProgram program,
			FiniteStateMachine finiteStateMachine,
			Interpreter interpreter,
			Map<Long, Long> heap,
			Stack<Long> stack,
			Map<Long, Long> labels,
			Stack<Long> subRoutines
			){
		
		State stackState = 
			createStackState(program, finiteStateMachine, stack);
			
		State flowState = 
			createFlowState(
				program, finiteStateMachine, interpreter, stack, labels, subRoutines);
			
		State impTabState =
			createIMPTabState(
				program, finiteStateMachine, stack, heap);
			
		State impState = 
			new InstructionModificationParameterState(
				program, finiteStateMachine, stackState, flowState, impTabState);	
			
		return impState;
	}

	public static State createIMPTabState(
		WhitespaceProgram program,
		FiniteStateMachine finiteStateMachine,
		Stack<Long> stack,
		Map<Long,Long> heap) {
		
		State arithmeticState =
			createArithmetricState(program, finiteStateMachine, stack);
				
		
		State ioState = 
			createIOState(program, finiteStateMachine, heap, stack); 
		
		State heapState = 
			createHeapState(program, finiteStateMachine, heap, stack);
			
		
		return new InstructionModificationParameterTabState(
			program, finiteStateMachine, arithmeticState, ioState, heapState);
	}

	public static IOState createIOState(
		WhitespaceProgram program,
		FiniteStateMachine finiteStateMachine,
		Map<Long, Long> heap,
		Stack<Long> stack) {
		
		State inputState =
			createInputState(program, finiteStateMachine, heap, stack);
		
		State outputState =
			createOutputState(program, finiteStateMachine, stack);
		
		return new IOState(
			program, finiteStateMachine, inputState, outputState);
	}

	public static State createInputState(
		WhitespaceProgram program,
		FiniteStateMachine finiteStateMachine,
		Map<Long, Long> heap,
		Stack<Long> stack) {
		
		return new InputState(program, finiteStateMachine, stack, heap);
	}
	
	public static State createOutputState(
		WhitespaceProgram program,
		FiniteStateMachine finiteStateMachine,
		Stack<Long> stack) {
		
		return new OutputState(program, finiteStateMachine, stack);
	}

	public static FlowState createFlowState(
		WhitespaceProgram program,
		FiniteStateMachine finiteStateMachine,
		Interpreter interpreter,
		Stack<Long> stack,
		Map<Long, Long> labels, 
		Stack<Long> subRoutines) {
		
		State flowLineFeedState = 
			createFlowLineFeedState(program, finiteStateMachine, interpreter);
		
		State flowSpaceState = 
			createFlowSpaceState(program, finiteStateMachine, labels, subRoutines);
		
		State flowTabState =
			createFlowTabState(program, finiteStateMachine, stack, labels,subRoutines);
		
		return new FlowState(
			program, finiteStateMachine, flowLineFeedState, flowSpaceState,	flowTabState);
	}

	public static FlowLineFeedState createFlowLineFeedState(
		WhitespaceProgram program, 
		FiniteStateMachine finiteStateMachine,
		Interpreter interpreter) {
		
		return new FlowLineFeedState(program, finiteStateMachine, interpreter);
	}

	public static State createFlowSpaceState(
		WhitespaceProgram program,
		FiniteStateMachine finiteStateMachine,
		Map<Long, Long> labels,
		Stack<Long> subRoutines) {
		
		return new FlowSpaceState(program, finiteStateMachine, labels, subRoutines);
	}
	
	public static State createFlowTabState(
		WhitespaceProgram program,
		FiniteStateMachine finiteStateMachine,
		Stack<Long> stack,
		Map<Long, Long> labels,
		Stack<Long> subRoutines) {
		
		return new FlowTabState(
			program, finiteStateMachine, stack, labels, subRoutines);
	}

	public static State createStackState(
		WhitespaceProgram program,
		FiniteStateMachine finiteStateMachine,
		Stack<Long> stack) {
		
		State stackLineState = 
			createStackLineState(program, finiteStateMachine, stack);
		
		State stackTabState = 
			createStackTabState(program, finiteStateMachine, stack);
		
		return new StackState(
			program, finiteStateMachine, stack, stackLineState, stackTabState);
	}

	public static State createStackTabState(
		WhitespaceProgram program,
		FiniteStateMachine finiteStateMachine,
		Stack<Long> stack) {
		
		return new StackTabState(program, finiteStateMachine, stack);
	}

	public static State createStackLineState(
		WhitespaceProgram program,
		FiniteStateMachine finiteStateMachine,
		Stack<Long> stack) {
		
		return new StackLineFeedState(program, finiteStateMachine, stack);
	}

	public static State createHeapState(
		WhitespaceProgram program,
		FiniteStateMachine finiteStateMachine,
		Map<Long, Long> heap,
		Stack<Long> stack) {
		
		return new HeapState(program, finiteStateMachine, stack, heap);
	}

	public static State createArithmetricState(
		WhitespaceProgram program,
		FiniteStateMachine finiteStateMachine,
		Stack<Long> stack){
		
		ArithmeticUnit arithmeticUnit =
			new ArithmeticUnit(stack);
		
		State arithmeticSpaceState =
			createArithmeticSpaceState(
				program, finiteStateMachine, arithmeticUnit);

		State arithmeticTabState =
			createArithmeticTabState(
				program, finiteStateMachine, arithmeticUnit);
		
		return  new ArithmeticState(
			program, 
			finiteStateMachine, 
			arithmeticSpaceState, 
			arithmeticTabState);
	}
	
	public static State createArithmeticSpaceState(
		WhitespaceProgram program,
		FiniteStateMachine finiteStateMachine,
		ArithmeticUnit arithmeticUnit){
			
		return new ArithmeticSpaceState(
			program, finiteStateMachine, arithmeticUnit);
	}

	public static State createArithmeticTabState(
		WhitespaceProgram program,
		FiniteStateMachine finiteStateMachine,
		ArithmeticUnit arithmeticUnit){
			
		return new ArithmeticTabState(
			program, finiteStateMachine, arithmeticUnit);
	}

}