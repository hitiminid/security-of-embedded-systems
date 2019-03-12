use std.textio.all;

entity hello_world is
end hello_world;

architecture behaviour of hello_world is
begin
	process
		variable l : line;
		variable buffer_in : line;

	begin
		write (l, String'("Hello world!"));
		writeline(output, l);
		readline(input, buffer_in);
		writeline(output, buffer_in);
		wait;
	end process;
end behaviour;
