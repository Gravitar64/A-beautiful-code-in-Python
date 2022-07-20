import hashlib


class Block():
  def __init__(self, nr, transaktionen, vorHash):
    self.nr = nr
    self.transaktionen = transaktionen
    self.vorHash = vorHash
    self.hash = self.generiereHash()

  def generiereHash(self):
    blockDaten = str(self.nr) + ''.join(self.transaktionen)+self.vorHash
    return hashlib.sha256(blockDaten.encode()).hexdigest()

  def __str__(self):
    erg = ''
    erg += f'Block Nr.     : {self.nr}\n'
    erg += f'vorh. Hash    : {self.vorHash}\n'
    erg += f'Transaktionen : {self.transaktionen}\n'
    erg += f'Hash          : {self.hash}\n'
    erg += f'tats. Hash    : {self.generiereHash()}\n'
    return erg


class BlockChain():
  def __init__(self):
    self.blocks = [Block(0, ['Genesis'], '00'*32)]

  def append(self, transaktionen):
    nr = len(self.blocks)
    vorHash = self.blocks[-1].hash
    self.blocks.append(Block(nr, transaktionen, vorHash)
                       )

  def __str__(self):
    return '\n'.join([str(block) for block in self.blocks])


chain = BlockChain()
chain.append(['Alice zahlt an Bob 0.1', 'Bob zahlt an Charlie 0.05'])
chain.append(['Charlie zahlt an Alice 0.2', 'Bob zahlt an Alice 0.4'])
print(chain)