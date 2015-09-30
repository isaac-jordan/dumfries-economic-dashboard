package uk.ac.glasgow.whitespace4j.test;

import static org.junit.Assert.*;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.util.Arrays;
import java.util.Collection;

import org.apache.log4j.PropertyConfigurator;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;

import uk.ac.glasgow.whitespace4j.CharacterSet;
import uk.ac.glasgow.whitespace4j.Interpreter;
import uk.ac.glasgow.whitespace4j.Main;
import uk.ac.glasgow.whitespace4j.WhitespaceProgram;

@RunWith(Parameterized.class)
public class InterpreterTestCase {
	
	@BeforeClass
	public static void setUpClass(){
		PropertyConfigurator.configure("log4j.properties");
	}
	
	@Parameters
	public static Collection<Object[]> paths() {
	
		
		Object[][] testData = {
			{CharacterSet.VISIBLE, "testset/visible/count.ws", "", "1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n"},
			{CharacterSet.VISIBLE, "testset/visible/hanoi.ws", "1", "Enter a number: 1 -> 3\r\n"},
			{CharacterSet.VISIBLE, "testset/visible/helloworld.ws", "", "Hello, world of spaces!\r\n"},
				
			{CharacterSet.DEFAULT, "testset/default/count.ws", "", "1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n"},
			{CharacterSet.DEFAULT, "testset/default/fact.ws", "6", "Enter a number: 6! = 720\r\n"},
			{CharacterSet.DEFAULT, "testset/default/fibonacci.ws", "6", "How many? 1\n1\n2\n3\n5\n8\n13\n21\n"},
			{CharacterSet.DEFAULT, "testset/default/name.ws", "Tim\n", "Please enter your name: Hello Tim\n\r\n"},
			{CharacterSet.DEFAULT, "testset/default/hanoi.ws", "1", "Enter a number: 1 -> 3\r\n"},				
			{CharacterSet.DEFAULT, "testset/default/helloworld.ws", "", "Hello, world of spaces!\r\n"}
		};
	
		return Arrays.asList(testData);
			
	};
		
	private CharacterSet characters;
	private String sourceFilePath;
	private String userInput;
	private String expectedOutput;
		
	public InterpreterTestCase(CharacterSet characters, String filePath, String userInput, String expectedOutput){
		this.characters = characters;
		this.sourceFilePath = filePath;
		this.userInput = userInput;
		this.expectedOutput = expectedOutput;
	}
	
	private ByteArrayOutputStream baos;
	private ByteArrayInputStream bais;
	private Interpreter interpreter;

	@Before
	public void setUp() throws Exception {
		
		String source = Main.readProgramSourceFile(sourceFilePath);
		WhitespaceProgram program = new WhitespaceProgram(source);
		
		baos = new ByteArrayOutputStream();
		bais = new ByteArrayInputStream(userInput.getBytes());
		
		interpreter = new Interpreter(program, characters, bais, baos);
	}

	@Test
	public void test() {
		interpreter.run();
		String actualOutput = new String(baos.toByteArray());		
			
		assertEquals(expectedOutput, actualOutput);
	}
}
