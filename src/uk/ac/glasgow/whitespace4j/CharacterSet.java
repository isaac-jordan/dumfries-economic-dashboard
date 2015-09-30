package uk.ac.glasgow.whitespace4j;

/**
 * Collates available whitespace program character sets.
 * @author tws
 *
 */
public enum CharacterSet {
	
	DEFAULT('\t', ' ', '\n'),
	VISIBLE('T', 'W', 'N');

	public Character getTab() {
		return tab;
	}

	public Character getSpace() {
		return space;
	}

	public Character getLineFeed() {
		return lineFeed;
	}

	private Character tab;
	private Character space;
	private Character lineFeed;

	private CharacterSet(
		Character tab, Character space, Character lineFeed) {
		
		this.tab = tab;
		this.space = space;
		this.lineFeed = lineFeed;
	}
	
	public Boolean contains(Character character){
		return character == tab || character == lineFeed || character == space;
	}
}