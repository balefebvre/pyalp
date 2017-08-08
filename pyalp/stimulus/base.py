class Stimulus(object):
    """Stimulus base class."""
    # TODO complete docstring.

    def __init__(self):

        pass

    def prompt_input_arguments(self):

        raise NotImplementedError()

    def display(self, device):

        raise NotImplementedError()
