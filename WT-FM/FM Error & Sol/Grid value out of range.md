## Error: The system is looking for a value outside the grid along the 0 (fps.lp) index

## Reasons: 
1. The funnel is not properly defined. 
2. MAXS > U_wall or MINS < L_wall 
3. Alignment is improperly set. 

## Solutions:
1. Define the funnel in a complete system which maybe taken after centering. Make sure no broken structure. 
2.  MAXS < U_wall and MINS > L_wall - This parameters should be followed. 
3. Make sure to take the ref structure (Probably taking CA atoms) from the same structure that is used for funnel definition.
