package uk.ac.glasgow.whitespace4j;

import org.apache.log4j.Logger;

/**
 * Abstract finite state machine state class, containing general functions for
 * transitions between states based on program instructions.
 * 
 * @author tws
 * 
 */
public abstract class State {
	
	protected static final Logger logger = Logger.getLogger(State.class);
	
	private Character tab;
	private Character space;
	private Character lineFeed; 
	
	private WhitespaceProgram program;

	private FiniteStateMachine finiteStateMachine;

	/**
	 * Constructs a new state for the specified finite state machine, operating
	 * on the specified program.
	 * 
	 * @param program
	 *            the whitespace program to interpret.
	 * @param finiteStateMachine
	 *            the host finite state machine for this state.
	 */
	public State (WhitespaceProgram program, FiniteStateMachine finiteStateMachine){
		this.program = program;
		
		this.finiteStateMachine = finiteStateMachine;
		
		CharacterSet characterSet = finiteStateMachine.getCharacterSet();
						
		tab = characterSet.getTab();
		space = characterSet.getSpace();
		lineFeed = characterSet.getLineFeed();
	}
	
	public void execute () throws InterpretWhitespaceException{
		Character token = this.getNextProgramToken();
			
		finiteStateMachine.addTokenToCurrentInstruction(token);
		
		Boolean scanMode = 
			finiteStateMachine.isInScanMode();
		
		if (token==space) doSpaceAction();
		else if (token==tab) doTabAction();
		else if (token==lineFeed) doLineFeedAction();
		else if (token==null && scanMode) return;
		else
			throw new InterpretWhitespaceException(program, this);			
	}
	
	/**
	 * @return this State's finite state machine.
	 */
	protected FiniteStateMachine getFiniteStateMachine() {
		return finiteStateMachine;
	}
	
	/**
	 * @return the whitespace program interpreted by this state.
	 */
	public WhitespaceProgram getProgram() {
		return program;
	}
	
	/**
	 * Interprets a signed number from the program content, beginning at the
	 * current counter position.
	 * 
	 * @return a signed Long value representation of the value read from the
	 *         current position in the program.
	 * @throws InterpretWhitespaceException
	 *             if the whitespace encoding is improper
	 */
	protected long interpretSignedNumber() throws InterpretWhitespaceException{
		return interpretNumber(true);
	}
	
	/**
	 * Interprets an unsigned number from the program content, beginning at the
	 * current counter position.
	 * 
	 * @return an unsigned Long value representation of the value read from the
	 *         current position in the program.
	 * @throws InterpretWhitespaceException
	 *             if the whitespace encoding is improper.
	 */
	protected long interpretUnsignedNumber() throws InterpretWhitespaceException{
		return interpretNumber(false);
	}	
	
	/**
	 * Interprets a number from the program content, beginning at the current
	 * counter position. The number may be read as either signed or unsigned.
	 * 
	 * @param isSigned
	 *            specifies whether the value should be interpreted as signed or
	 *            not.
	 * @return A Long value representation of the (optionally signed) value read
	 *         from the current position in the program.
	 * @throws InterpretWhitespaceException
	 *             if the whitespace encoding of the number is improper.
	 */
	private Long interpretNumber(Boolean isSigned) throws InterpretWhitespaceException{
		
		finiteStateMachine.addTokenToCurrentInstruction(':');
		
		Long result = 0l;
		Integer signMultiplier = 1;
		
		if (isSigned){
	
			Character sign = getNextProgramToken();
			
			finiteStateMachine.addTokenToCurrentInstruction(sign);
			
			if (sign==tab) signMultiplier = -1;
			else if (sign==space) signMultiplier = 1;
			else 
				throw new InterpretWhitespaceException(program, this);		
		}
		
		Character c = getNextProgramToken();
		
		while(c != lineFeed){
			
			finiteStateMachine.addTokenToCurrentInstruction(c);
			
			result *=2;
			if (c==tab) result++;
			else if (c==space);
			else 
				throw new InterpretWhitespaceException(program, this);
			
			c = getNextProgramToken();

		}
		
		return result*signMultiplier;
	}
	
	private Character getNextProgramToken(){
		Character token = program.getTokenAndIncrement();
		
		while( !( token==tab || token==lineFeed || token==space || token==null ) )
			token = program.getTokenAndIncrement();
		
		return token;
	}
	
	protected void doLineFeedAction() throws InterpretWhitespaceException {
		throw new InterpretWhitespaceException(program, this);
	}

	protected void doSpaceAction() throws InterpretWhitespaceException {
		throw new InterpretWhitespaceException(program, this);	
	}

	protected void doTabAction() throws InterpretWhitespaceException {
		throw new InterpretWhitespaceException(program, this);
	}
}