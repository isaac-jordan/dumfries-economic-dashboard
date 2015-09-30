package uk.ac.glasgow.whitespace4j;

import org.apache.log4j.Logger;

/**
 * Wrapper class for inspecting a whitespace program represented as a String.
 * @author tws
 *
 */
public class WhitespaceProgram {
	
	private static final Logger logger = Logger.getLogger(WhitespaceProgram.class);
	
	/** The whitespace program source */
	private String source;
	
	/** The program counter */
	private Long counter;
	
	/**
	 * Constructs a new WhiteSpaceProgram instance.
	 * 
	 * @param source
	 *            the whitespace program to be interpreted.
	 */
	public WhitespaceProgram (String source){
		this.source = source;
		this.reset();
	}
	
	/**
	 * @return the current position in the program.
	 */
	public Long getCounter(){
		return counter;
	}
	
	/**
	 * Moves the program counter to the specified position.
	 * @param position the new position for the counter
	 */
	public void jump(Long position){
		logger.debug(
			"Jump request to position ["+position+"] "
			+ "from position ["+ counter +"].");
		
		counter = position;
	}
	
	/**
	 * Gets the token at the current position and then increments the program
	 * counter.
	 * 
	 * @return the token at the current position of the program counter.
	 */
	public Character getTokenAndIncrement (){
		if (counter < source.length())
			return source.charAt((counter++).intValue());
		else
			return null;
	}
	
	/**
	 * @return the token at the current position.
	 */
	public Character getCurrentToken(){
		return source.charAt(counter.intValue());
	}
	
	/**
	 * @return true if the program counter is beyond the last token in the
	 *         program string.
	 */
	public Boolean isAtEnd(){
		return counter >= source.length();
	}
	
	/**
	 * Places the counter at the start of the program string.
	 */
	public void reset(){
		counter = 0l;
	}
}
