const { task } = require("hardhat/config");

require("@nomiclabs/hardhat-waffle");

task("accounts", "Prints a list of accounts", async (taskArgs, hre) => {
  const acounts = await hre.ethers.getSigners();

  for (const account of accounts) {
    console.log(account.address);
  }
});


/**
 * @type import('hardhat/config').HardhatUserConfig
 */
module.exports = {
  solidity: "0.8.7",
};
