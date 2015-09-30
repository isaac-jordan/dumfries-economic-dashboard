package uk.ac.glasgow.whitespace4j.arithmetic.test;

import static org.junit.Assert.*;

import java.util.Arrays;
import java.util.Collection;
import java.util.Stack;

import org.apache.log4j.PropertyConfigurator;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;

import uk.ac.glasgow.whitespace4j.CharacterSet;
import uk.ac.glasgow.whitespace4j.FiniteStateMachine;
import uk.ac.glasgow.whitespace4j.InterpretWhitespaceException;
import uk.ac.glasgow.whitespace4j.State;
import uk.ac.glasgow.whitespace4j.WhitespaceProgram;
import uk.ac.glasgow.whitespace4j.factory.StateFactory;

@RunWith(Parameterized.class)
public class ArithmeticStateTestCase {
	
	@BeforeClass
	public static void setUpClass(){
		PropertyConfigurator.configure("log4j.properties");
	}
	
	private CharacterSet characterSet = CharacterSet.VISIBLE;

	private State state;
	private Stack<Long> stack;
	
	private WhitespaceProgram program;
	
	@Parameters
	public static Collection<Object[]> paths() {
	
		Object[][] testData = {
				{"WW",new Long[]{4l, 5l}, new Long[]{9l}}, // addition
				{"WT",new Long[]{4l, 5l}, new Long[]{-1l}}, // subtraction
				{"WN",new Long[]{4l, 5l}, new Long[]{20l}}, // multiplication
				{"TW",new Long[]{24l, 6l}, new Long[]{4l}}, // division
				{"TT",new Long[]{25l, 4l}, new Long[]{1l}}, // modulo
				
		};
	
		return Arrays.asList(testData);
			
	};
	
	private String programSource;
	private Long[] stackStartValues;
	private Long[] stackEndValues;
	
	public ArithmeticStateTestCase(
		String programSource, Long[] stackStartValues, Long[] stackEndValues){
		this.programSource = programSource;
		this.stackStartValues = stackStartValues;
		this.stackEndValues = stackEndValues;
	}
	
	@Before
	public void setUp() throws Exception {
		
		stack = new Stack<Long>();
		program = new WhitespaceProgram(programSource);
		
		FiniteStateMachine finiteStateMachine =
			new MockWhitespaceFSM(characterSet);
		
		state = StateFactory.createArithmetricState(program, finiteStateMachine, stack);
		
		for (Long value: stackStartValues) stack.add(value);
	}

	@Test
	public void testArithmeticState(){
		while (!program.isAtEnd()) 		
			try {
				state.execute();
			} catch (InterpretWhitespaceException e) {
				fail();
				e.printStackTrace();
			}
		
		for (Long expectedOutput : stackEndValues){
			Long actualOutput = stack.pop(); 
			assertEquals(expectedOutput, actualOutput);
		}
	}

}
