library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity a51_tb is
end a51_tb;

architecture behav  of a51_tb is

  constant clock_period : time := 10 ns;

  signal clock : STD_LOGIC := '0';

  signal q1 : STD_LOGIC_VECTOR(18 downto 0) := (OTHERS => '0');
  signal q2 : STD_LOGIC_VECTOR(21 downto 0) := (OTHERS => '0');
  signal q3 : STD_LOGIC_VECTOR(22 downto 0) := (OTHERS => '0');
  signal load : STD_LOGIC := '0';

  signal o : STD_LOGIC;

component a51
  port(
    clk : in STD_LOGIC;
    ld : in STD_LOGIC;
    short_data : in STD_LOGIC_VECTOR(18 downto 0);
    medium_data : in STD_LOGIC_VECTOR(21 downto 0);
    long_data : in STD_LOGIC_VECTOR(22 downto 0);
    R : out STD_LOGIC
  );
end component;
  for UUT1 : a51 use entity work.a51(system);

begin

  UUT1 : a51 port map (clk => clock, ld => load, short_data => q1, medium_data => q2, long_data  => q3, R => o);

  -- this will run infinitely, stopping every few ns
  clocker : process
  begin
    clock <= not clock;
    wait for clock_period/2;
  end process;

  init : process
  begin
    load <= '1';

    q1 <= "1010101010101010101";
    q2 <= "1010101010101010101010";
    q3 <= "10101010101010101010101";

    wait until clock'event and clock = '0';
    load <= '0';

  wait;
end process;

END behav;
