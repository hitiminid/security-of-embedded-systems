library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity a51 is
  Port ( clk : in STD_LOGIC;
         ld  : in STD_LOGIC;
         short_data : in STD_LOGIC_VECTOR(18 downto 0) := (OTHERS => '0');
         medium_data : in STD_LOGIC_VECTOR(21 downto 0) := (OTHERS => '0');
         long_data : in STD_LOGIC_VECTOR(22 downto 0) := (OTHERS => '0');
         R : out STD_LOGIC
  );
end a51;

ARCHITECTURE system OF a51 IS
 signal short_is : STD_LOGIC_VECTOR(18 downto 0) := (OTHERS => '0');
 signal medium_is : STD_LOGIC_VECTOR(21 downto 0) := (OTHERS => '0');
 signal long_is : STD_LOGIC_VECTOR(22 downto 0) := (OTHERS => '0');
BEGIN
  PROCESS(clk, ld, short_data, medium_data, long_data)
    BEGIN
      if(ld = '1')
      then
        short_is <= short_data;
        medium_is <= medium_data;
        long_is <= long_data;
      elsif(clk'event and clk = '1')
      then
        if (short_is(8) = medium_is(10))
        then
          short_is(18 downto 1) <= short_is(17 downto 0);
          short_is(0) <= short_is(18) xor short_is(17) xor short_is(16) xor short_is(13);

          medium_is(21 downto 1) <= medium_is(20 downto 0);
          medium_is(0) <= medium_is(21) xor medium_is(20);

          if (short_is(8) = long_is(10))
          then

            long_is(22 downto 1) <= long_is(21 downto 0);
            long_is(0) <= long_is(22) xor long_is(21) xor long_is(20) xor long_is(7);

          end if;
        elsif (short_is(8) = long_is(10))
        then

          short_is(18 downto 1) <= short_is(17 downto 0);
          short_is(0) <= short_is(18) xor short_is(17) xor short_is(16) xor short_is(13);

          long_is(22 downto 1) <= long_is(21 downto 0);
          long_is(0) <= long_is(22) xor long_is(21) xor long_is(20) xor long_is(7);

        else
          medium_is(21 downto 1) <= medium_is(20 downto 0);
          medium_is(0) <= medium_is(21) xor medium_is(20);

          long_is(22 downto 1) <= long_is(21 downto 0);
          long_is(0) <= long_is(22) xor long_is(21) xor long_is(20) xor long_is(7);

        end if;
    end if;
  END PROCESS;


  R <= long_is(22) xor medium_is(21) xor short_is(18);

END system;
