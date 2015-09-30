package uk.ac.glasgow.whitespace4j.arithmetic;

import java.util.Stack;

public class ArithmeticUnit {

	private Stack<Long> stack;

	public ArithmeticUnit(Stack<Long> stack) {
		this.stack = stack;
	}
	
	protected void doOperation(OpFlag opFlag)
			throws Exception{
			
			Long e1 = stack.pop();
			Long e2 = stack.pop();
			
			switch (opFlag) {
			
			case MULTIPLICATION:
				stack.push(e2*e1);
				break;
				
			case ADDITION: 
				stack.push(e2+e1);
				break;
				
			case SUBTRACTION: 
				stack.push(e2-e1);
				break;
				
			case DIVISION: 
				stack.push(e2 / e1);
				break;
					
			case MODULO:
				stack.push(e2 % e1); 
				break;
				
			default: 
				throw 
					new Exception(
						"Unknown aritmetric operator ["+opFlag+"]");
			}
		}


}
