const { expect } = require("chai");
const { ethers } = require("hardhat");

let owner;
let addr1;
let addr2;
let minter;
const provider = ethers.provider;
beforeEach(async () => {
    [owner, addr1, addr2] = await ethers.getSigners();

    let minterContract = await ethers.getContractFactory("NftMinter");
    minter = await minterContract.connect(owner).deploy("collectionName", "CN");
    await minter.enableBatch(100, ethers.utils.parseEther("1"));

});


describe("Minter Contract", () => {
    it("have 100 total currently mintable", async () => {
        let amount = await minter.totalCurrentlyMintable();
        expect(amount == 100);
    })

    it("Allow minting of one NFT", async () => {
        await minter.connect(addr1).mint(1, { value: ethers.utils.parseEther("1") });
        let balance = await minter.balanceOf(addr1.address)
        expect(balance == 1);
    })

    it("Have 101 mintable after enabling 100 more", async () => {
        await minter.enableBatch(100, 1);
        let amount = await minter.totalCurrentlyMintable();
        expect(amount == 101);
    })

    it("should have transfered 1 eth to owner", async () => {
        let balance = await provider.getBalance(owner.address);
        let formatted = ethers.utils.formatEther(balance);
        expect(formatted > 100.5);
    })

    it("should not allow more than 10 to be minted for the owner", async () => {
        await expect(minter.connect(owner).mint(11)).to.be.revertedWith("You can not mint more than 10 at a time");
    })


    it("should not allow more than 10 to be minted for a customer", async () => {
        await expect(minter.connect(addr1).mint(11, { value: ethers.utils.parseEther("11") })).to.be.revertedWith('You can not mint more than 10 at a time');
    })

    it("should revert if 1 eth is sent to mint 2 NFTs (1 eth test amount)", async () => {
        await expect(minter.connect(addr1).mint(2, { value: ethers.utils.parseEther("1") })).to.be.revertedWith("Not enough ether was sent");
    })

    it("should allow changing the ownership of the contract", async () => {
        await minter.connect(owner).setOwner(addr1.address);
        expect(await minter.owner()).to.equal(addr1.address);
    })

    it("Should not allow the original owner to change ownership again", async () => {
        await minter.connect(owner).setOwner(addr1.address);
        await expect(minter.connect(owner).setOwner(owner.address)).to.be.revertedWith("Only the owner can call this function")
    })

    it("Should be charging 1 eth per mint", async () => {
        await expect(await minter.getPrice()).to.equal(ethers.utils.parseEther("1"))
    })

    it("Should return 1 total minted after 1 mint", async () => {
        await minter.connect(owner).mint(1);
        expect(await minter.getTotalMinted()).to.equal(1);
    })

    it("Should revert on minting the 101st NFT", async () => {
        for (i = 0; i < 10; i++) {
            await minter.connect(owner).mint(10);
        }
        await expect(minter.connect(owner).mint(1)).to.be.revertedWith("Can not mint more than the limit")
    })

    it("Should not allow minting if the killswitch is flipped", async () => {
        await minter.connect(owner).flipSaleState();
        await expect(minter.connect(owner).mint(1)).to.be.revertedWith("This function is not available at this time");
    })

    it("Should not allow someone other than the owner to change the owner", async () => {
        await expect(minter.connect(addr1).setOwner(addr1.address)).to.be.revertedWith("Only the owner can call this function");
    })
})