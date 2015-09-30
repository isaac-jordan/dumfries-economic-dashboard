package uk.ac.glasgow.whitespace4j;

/**
 * Indicates that an error has occurred during the interpretation of the current
 * whitespace program.
 * 
 * @author tws
 * 
 */
public class InterpretWhitespaceException extends Exception {
	
	/****/
	private static final long serialVersionUID = -3813716494184795541L;

	/**
	 * 
	 * @param program
	 *            the whitespace program in which the exception occurred
	 * @param state
	 *            the finite state machine state of the interpreter in which the
	 *            exception occurred.
	 *            
	 * @param t the underlying exception that caused the error.
	 */
	public InterpretWhitespaceException(WhitespaceProgram program, State state, Throwable t){
		super(createMessage(program, state), t);
	}
	

	/**
	 * 
	 * @param program
	 *            the whitespace program in which the exception occurred
	 * @param state
	 *            the finite state machine state of the interpreter in which the
	 *            exception occurred.
	 */
	public InterpretWhitespaceException(WhitespaceProgram program, State state){
		super(createMessage(program, state));
	}
		
	private static String createMessage(
		WhitespaceProgram program, State state){
		
		Character character = program.getCurrentToken();
		Long position = program.getCounter();
		
		String stateString =
			State.class.getSimpleName();
					
		String message =
			"Unexpected character [%s] at position [%s], "
			+ "during execution of state [%s].";
			
		return 
			String.format(message, character, position, stateString);
	}
}
