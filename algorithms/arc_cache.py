import time
from collections import OrderedDict
from core.cache_abc import Cache


class ARCCache(Cache):
    """
    Implementação do algoritmo de cache Adaptive Replacement Cache (ARC).
    O ARC equilibra dinamicamente entre LRU (recência) e LFU (frequência).
    """

    def __init__(self, capacity: int = 10, reader_func=None):
        if capacity <= 0:
            raise ValueError("A capacidade do cache deve ser maior que zero.")
        if reader_func is None:
            raise ValueError("Uma função de leitura (reader_func) deve ser fornecida.")

        self.capacity = capacity
        self.read_from_slow_disk = reader_func

        # Parâmetro adaptativo 'p'. Controla o tamanho alvo da lista T1 (recência).
        self.p = 0

        # T1: Cache para itens vistos apenas uma vez (LRU - Recência)
        self.t1 = OrderedDict()
        # T2: Cache para itens vistos mais de uma vez (LFU - Frequência)
        self.t2 = OrderedDict()

        # B1: Lista "fantasma" de chaves recentemente removidas de T1
        self.b1 = OrderedDict()
        # B2: Lista "fantasma" de chaves recentemente removidas de T2
        self.b2 = OrderedDict()

    def _replace(self, text_id: int):
        """
        Função de evicção chamada em um cache miss quando o cache está cheio.
        Esta é a lógica central que adapta o tamanho das listas.
        """
        # Se T1 não está vazia e (T1 é maior que o alvo 'p' OU (o item a ser removido está em B2 e T1 tem o mesmo tamanho de 'p'))
        if self.t1 and (len(self.t1) > self.p or (text_id in self.b2 and len(self.t1) == self.p)):
            # Remove o item LRU de T1 e o move para a lista fantasma B1
            old_key, _ = self.t1.popitem(last=False)
            self.b1[old_key] = None
            if len(self.b1) > self.capacity - self.p:
                self.b1.popitem(last=False)
        else:
            # Remove o item LRU de T2 e o move para a lista fantasma B2
            old_key, _ = self.t2.popitem(last=False)
            self.b2[old_key] = None
            if len(self.b2) > self.p:
                self.b2.popitem(last=False)

    def access(self, text_id: int) -> tuple[bool, str, float]:
        """
        Acessa um texto, aplicando a lógica adaptativa do ARC.
        """
        start_time = time.perf_counter()

        # CASO 1: Cache Hit (o texto está em T1 ou T2)
        if text_id in self.t1 or text_id in self.t2:
            is_hit = True
            # Se estava em T1, foi acessado uma segunda vez. Mova para T2 (mais frequente).
            if text_id in self.t1:
                content = self.t1.pop(text_id)
                self.t2[text_id] = content
            # Se já estava em T2, apenas mova para o final (mais recente).
            else:
                content = self.t2[text_id]
                self.t2.move_to_end(text_id)

        # CASO 2: Cache Miss
        else:
            is_hit = False
            content = self.read_from_slow_disk(text_id)

            # SUB-CASO 2.1: O item estava na lista fantasma B1 (era recente, mas foi removido)
            if text_id in self.b1:
                # Adaptação: aumenta o tamanho alvo 'p' para T1 (dá mais importância à recência).
                self.p = min(self.capacity, self.p + max(len(self.b2) / len(self.b1), 1))
                self._replace(text_id)
                self.b1.pop(text_id, None)
                self.t2[text_id] = content  # Move para a lista de frequentes

            # SUB-CASO 2.2: O item estava na lista fantasma B2 (era frequente, mas foi removido)
            elif text_id in self.b2:
                # Adaptação: diminui o tamanho alvo 'p' para T1 (dá mais importância à frequência).
                self.p = max(0, self.p - max(len(self.b1) / len(self.b2), 1))
                self._replace(text_id)
                self.b2.pop(text_id, None)
                self.t2[text_id] = content  # Move para a lista de frequentes

            # SUB-CASO 2.3: Miss completo (item nunca visto antes)
            else:
                # Se o cache está cheio (T1 + T2)
                if len(self.t1) + len(self.t2) >= self.capacity:
                    # Se T1 está cheio, remova da lista fantasma B1 para dar espaço
                    if len(self.t1) < self.capacity:
                        self.b1.popitem(last=False) if self.b1 else None
                    self._replace(text_id)

                # Adiciona o novo item em T1 (visto pela primeira vez)
                self.t1[text_id] = content

        end_time = time.perf_counter()
        access_time = end_time - start_time

        return is_hit, content, access_time

    def __str__(self) -> str:
        """ Representação em string do estado do cache para a interface. """
        # Une as chaves de T1 e T2 para uma visualização consolidada
        all_keys = list(self.t1.keys()) + list(self.t2.keys())
        items = ', '.join(map(str, all_keys))
        return f"ARCCache (Size: {len(all_keys)}/{self.capacity}, p={self.p:.1f}) -> [{items}]"
    
