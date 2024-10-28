## Anchors in Document Example

<br />

### Introduction

<br />

This example demonstrates how to use special anchors in the document of a function. There are two types of parameter anchors:

<br />

- **Parameter Anchors**: This type of anchor is used to navigate to a specific parameter widget. When user clicks on a parameter
anchor, the current FnExecuteWindow will expand the corresponding parameter group and scroll to the widget of the specific
parameter and highlight it. Parameter anchors are created using the **#param=<PARAMETER_NAME>** syntax, e.g. **#param=param_a**.

<br />

- **Group Anchors**: This type of anchor is used expand the specific parameter group. When user clicks on a group anchor,
the corresponding parameter group will be expanded and the other parameter groups will be collapsed. 
This type of anchor is created using the **#group=[GROUP_NAME]** syntax, e.g. **#group=Group-A**. **#group=** is a special group
anchor that will expand the default parameter group (which is usually named "Main Parameters")

<br />

Parameter and group anchors are very useful if there are many parameters in a function and user wants to quickly navigate
to a specific parameter widget. The Section below shows an example of how to use parameter and group anchors.

<br />

### Demonstration

<br />

[Group-A](#group=Group-A)

- [a](#param=a): This is the description of parameter a.
- [b](#param=b): This is the description of parameter b.
- [c](#param=c): This is the description of parameter c.
- [d](#param=d): This is the description of parameter d.

<br />

[Group-B](#group=Group-B)

- [e](#param=e): This is the description of parameter e.
- [f](#param=f): This is the description of parameter f.
- [g](#param=g): This is the description of parameter g.
- [h](#param=h): This is the description of parameter h.

<br />

[Group-C](#group=Group-C)

- [i](#param=i): This is the description of parameter i.
- [j](#param=j): This is the description of parameter j.
- [k](#param=k): This is the description of parameter k.
- [l](#param=l): This is the description of parameter l.

<br />

[Main Parameters](#group=)

- [m](#param=m): This is the description of parameter m.
- [n](#param=n): This is the description of parameter n.
- [o](#param=o): This is the description of parameter o.
- [p](#param=p): This is the description of parameter p.

