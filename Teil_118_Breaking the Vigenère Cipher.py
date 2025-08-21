import itertools as itt, collections as coll, time


def encrypt(text, key):
  return "".join([v2l(l2v(a) + l2v(b)) for a, b in zip(text, itt.cycle(key))])


def decrypt(text, key):
  return "".join([v2l(l2v(a) - l2v(b)) for a, b in zip(text, itt.cycle(key))])


def get_key_length(text, max_key_len):
  coincedences = [sum([a == b for a, b in zip(text, text[i:])]) for i in range(1, max_key_len)]
  return coincedences.index(max(coincedences)) + 1


def get_key(text, key_len, commons):
  key = ""
  for i in range(key_len):
    frequence = coll.Counter(text[i::key_len])
    scores = [sum(frequence[v2l(l2v(c) + i)] for c in commons) for i in range(26)]
    key += v2l(scores.index(max(scores)))
  return key


l2v = lambda x: ord(x) - 65
v2l = lambda x: chr(x % 26 + 65)

time_start = time.perf_counter()
ciphertext = "MOMUDEKAPVTQEFMOEVHPAJMIICDCTIFGYAGJSPXYALUYMNSMYHVUXJELEPXJFXGCMJHKDZRYICUHYPUSPGIGMOIYHFWHTCQKMLRDITLXZLJFVQGHOLWCUHLOMDSOEKTALUVYLNZRFGBXPHVGALWQISFGRPHJOOFWGUBYILAPLALCAFAAMKLGCETDWVOELJIKGJBXPHVGALWQCSNWBUBYHCUHKOCEXJEYKBQKVYKIIEHGRLGHXEOLWAWFOJILOVVRHPKDWIHKNATUHNVRYAQDIVHXFHRZVQWMWVLGSHNNLVZSJLAKIFHXUFXJLXMTBLQVRXXHRFZXGVLRAJIEXPRVOSMNPKEPDTLPRWMJAZPKLQUZAALGZXGVLKLGJTUIITDSUREZXJERXZSHMPSTMTEOEPAPJHSMFNBYVQUZAALGAYDNMPAQOWTUHDBVTSMUEUIMVHQGVRWAEFSPEMPVEPKXZYWLKJAGWALTVYYOBYIXOKIHPDSEVLEVRVSGBJOGYWFHKBLGLXYAMVKISKIEHYIMAPXUOISKPVAGNMZHPWTTZPVXFCCDTUHJHWLAPFYULTBUXJLNSIJVVYOVDJSOLXGTGRVOSFRIICTMKOJFCQFKTINQBWVHGTENLHHOGCSPSFPVGJOKMSIFPRZPAASATPTZFTPPDPORRFTAXZPKALQAWMIUDBWNCTLEFKOZQDLXBUXJLASIMRPNMBFZCYLVWAPVFQRHZVZGZEFKBYIOOFXYEVOWGBBXVCBXBAWGLQKCMICRRXMACUOIKHQUAJEGLOIJHHXPVZWJEWBAFWAMLZZRXJEKAHVFASMULVVUTTGK"
key_len = get_key_length(ciphertext, 20)
key = get_key(ciphertext, key_len, "ETAOIN")
duration = time.perf_counter() - time_start
print(decrypt(ciphertext, key))
print(f"Cracked in {duration:.4f} sec.")
