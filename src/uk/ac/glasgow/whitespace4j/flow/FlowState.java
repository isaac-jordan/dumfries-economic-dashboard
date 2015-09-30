package uk.ac.glasgow.whitespace4j.flow;

import uk.ac.glasgow.whitespace4j.FiniteStateMachine;
import uk.ac.glasgow.whitespace4j.InterpretWhitespaceException;
import uk.ac.glasgow.whitespace4j.State;
import uk.ac.glasgow.whitespace4j.WhitespaceProgram;

public class FlowState extends State {
	
	private State flowLineFeed;
	private State flowSpace;
	private State flowTab;
	
	public FlowState(
		WhitespaceProgram program, 
		FiniteStateMachine finiteStateMachine, 
		State flowLineFeed, 
		State flowSpace, 
		State flowTab) {
		
		super(program, finiteStateMachine);	
		this.flowLineFeed = flowLineFeed;
		this.flowSpace = flowSpace;
		this.flowTab = flowTab;

	}

	@Override
	protected void doLineFeedAction() throws InterpretWhitespaceException {
		//logger.debug(name+": doing LF action.");
		flowLineFeed.execute();
	}

	@Override
	protected void doSpaceAction() throws InterpretWhitespaceException {
		//logger.debug(name+": doing SP action.");
		flowSpace.execute();
	}

	@Override
	protected void doTabAction() throws InterpretWhitespaceException {
		//logger.debug(name+": doing TA action.");
		flowTab.execute();
	}

}
