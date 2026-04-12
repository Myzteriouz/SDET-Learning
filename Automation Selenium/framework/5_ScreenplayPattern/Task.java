package com.framework.screenplay.core;

/**
 * The 'What' in Screenplay.
 * A Task is a high-level business goal (e.g., Login, Add To Cart) 
 * made up of smaller low-level Interactions (e.g., Click, Type).
 */
public interface Task {
    void performAs(Actor actor);
}
